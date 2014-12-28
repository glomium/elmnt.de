#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import project

import os


# SETTINGS ====================================================================


PROJECT = "FIXME"

APPS = [
    "FIXME",
]

DEPLOY = {
    'dev': {
        'ssh_host': 'elmnt-server',
        'basedir': '/var/www/django_projects/%s' % PROJECT,
    },
    'prod': {
        'ssh_host': 'igelware',
        'basedir': '/var/www/django_projects/%s' % PROJECT,
    }
}

# env for production (disables push for this env)
PRODUCTION = None

COPY_DB_EXCLUDE = [
    '', # keep me, so we can use join
    'contenttypes', # use natural keys instead
    'auth.permission', # use natural keys instead
    'sessions', # no need for this data
    'admin.logentry', # no need for this data
    'easy_thumbnails', # FIXME uncomment if using easy_thumbnails
]

@task
def dev():
    set_env("dev")

@task
def prod():
    set_env("prod")

BASEDIR = os.path.dirname( env.real_fabfile )
env.use_ssh_config = True


# LOCAL Methods ===============================================================


@task
def static():
    """
    complies and copies static files
    """
    js()
    css()
    with lcd(BASEDIR):
        for app in APPS:
            local('cp submodules/bootstrap/fonts/glyphicons-halflings-regular* media/fonts/')


@task
def css():
    """
    compiles and copies css
    """
    with lcd(BASEDIR):
        for app in APPS:
            local('lessc less/%s.less > bootstrap.css' % app)
            local('yui-compressor --type css -o media/css/%s.min.css bootstrap.css' % app)
        local('rm bootstrap.css')


@task
def js():
    """
    compiles and copies js
    """
    with lcd(BASEDIR):
        local('cp submodules/bootstrap/dist/js/bootstrap.min.js media/js/')
        for app in APPS:
            local('yui-compressor --type js -o media/js/%s.min.js js/%s.js' % (app, app))


@task
def watchstatic():
    """
    compiles and copies less and js - if changed
    """
    import pyinotify

    static()
    puts("========= DONE ==========")

    wm = pyinotify.WatchManager()

    excl_filter = pyinotify.ExcludeFilter([
        r'^\..*\.swp$',
        r'^\..*\.swx$',
    ])
    inc_filter = pyinotify.ExcludeFilter([
        r'.*\.less$',
        r'.*\.js$',
    ])

    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            if inc_filter(event.name):
                static()
                puts("========= DONE ==========")

    handler = EventHandler()

    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(
        [BASEDIR+'/js', BASEDIR+'/less'],
        pyinotify.ALL_EVENTS,
        rec=True,
        exclude_filter=excl_filter,
    )
    with settings(warn_only=True):
        notifier.loop()


@task
def init():
    """
    initialize apps
    """
    with lcd(BASEDIR):
        if not os.path.exists("media"):
            local("mkdir media")
            local("mkdir media/js")
            local("mkdir media/css")
            local("mkdir media/fonts")
        if not os.path.exists("static"):
            local("mkdir static")
        if not os.path.exists("less"):
            local("mkdir less")
        if not os.path.exists("js"):
            local("mkdir js")
        for app in APPS:
            if not os.path.exists(app) and not os.path.isdir(app):
                if not os.path.exists("project_template"):
                    local("git checkout project_template -- project_template")
                local("mv project_template %s" % app)
                local("git rm -r project_template")
                local("sed -i 's/{{ APP }}/%s/g' %s/settings.py" % (app, app))
                local("sed -i 's/{{ APP }}/%s/g' %s/wsgi.py" % (app, app))

            if not os.path.exists('less/%s.less' % app):
                local("touch less/%s.less" % app)

            if not os.path.exists('js/%s.js' % app):
                local("touch js/%s.js" % app)


@task
def export_local_db(app=None):
    '''
    Export local database into fixtures_live.json
    '''
    with lcd(BASEDIR):
        managepy('dumpdata -n --indent=1 %s > fixtures_local.json' % (' -e '.join(COPY_DB_EXCLUDE)), app)


@task
def start(app=None):
    """
    starts the project locally
    """
    managepy('runserver 0.0.0.0:8000', app)


@task
def shell(app=None):
    """
    starts a shell locally
    """
    managepy('shell', app)


@task
def test(app=None):
    """
    starts a test locally
    """
    managepy('test', app)


@task
def install():
    """
    installs the project locally
    """
    with lcd(BASEDIR): 
        local('rm -f %s/database.sqlite' % PROJECT)
        managepy('migrate --noinput')

        pull_db()
        pull_media()

        if os.path.exists('fixtures_live.json'):
            managepy('loaddata fixtures_live.json')
        else:
            managepy('createsuperuser')

        managepy('collectstatic --noinput')


# REMOTE Methods ==============================================================


@task
def push_db():
    """
    Copy the production DB from local to remote
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    if PRODUCTION and PRODUCTION == env.CFG['env']:
        puts("SKIPPING push_db: Not allowed to push to production")
        return False

    with lcd(BASEDIR):
        tmp = run('mktemp -d')
        put('fixtures_live.json', tmp)
        sudo('chown -R %s %s' % (env.CFG["user"], tmp))
        managepy('flush --no-initial-data --noinput', remote=True)
        managepy('loaddata %s/fixtures_live.json' % tmp, remote=True)
        sudo('rm -rf %s' % tmp)


@task
def pull_db():
    """
    Copy the production DB from remote to local
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    with lcd(BASEDIR):
        tmp = sudo('mktemp', user=env.CFG["user"], group=env.CFG["group"])
        managepy('dumpdata -n --indent=1 %s > %s' % (' -e '.join(COPY_DB_EXCLUDE), tmp), remote=True)
        get(tmp, 'fixtures_live.json')
        sudo('rm %s' % tmp)
        managepy('loaddata fixtures_live.json')


@task
def push_media():
    """
    Copy the production media from local to remote
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    if PRODUCTION and PRODUCTION == env.CFG['env']:
        puts("SKIPPING push_media: Not allowed to push to production")
        return False

    # TODO work with tmp directories on remote

    project.rsync_project(
        remote_dir=env.CFG['basedir'] + '/media',
        local_dir=BASEDIR + '/media/',
        upload=True,
        delete=True,
    )


@task
def pull_media():
    """
    Copy the production media from remote to local
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    # TODO work with tmp directories on remote

    project.rsync_project(
        remote_dir=env.CFG['basedir'] + '/media/',
        local_dir=BASEDIR + '/media',
        upload=False,
    )


@task
def pull():
    pull_media()
    pull_db()


@task
def push():
    push_media()
    push_db()


@task
def deploy():
    if not hasattr(env, 'CFG'):
        puts("You should load an environment!")

    # this is semi okay ... is syncs all projects, which is a bit overhead,
    # but the salt state-layout requires this (TODO)
    # better: sudo('salt-call state.sls projects.django')
    sudo('salt-call state.highstate')


# HELPER Methods ==============================================================


def set_env(e):
    setattr(env, 'CFG', DEPLOY[e])

    # store the active environment's key
    env.CFG['env'] = e

    # set hosts
    env.hosts = [env.CFG['ssh_host'],]

    # get and save user and group from basedir on remote
    with settings(hide('running', 'stdout'), host_string=env.CFG['ssh_host']):
        run_as = sudo('stat -c "%%U %%G" %s' % env.CFG['basedir'])
    env.CFG['user'], env.CFG['group'] = run_as.split(' ')


def managepy(cmd, app=None, remote=False):
    """
    Helper: run a management command remotely.
    """
    if not app:
        app = APPS[0]

    if remote:
        with cd(env.CFG['basedir']):
            sudo(
                'export DJANGO_SETTINGS_MODULE=%s.settings && virtenv/bin/python manage.py %s' % (
                    app,
                    cmd
                ),
                user=env.CFG["user"],
                group=env.CFG["group"],
            )
    else:
        with lcd(BASEDIR):
            local(
                'export DJANGO_SETTINGS_MODULE=%s.settings && virtenv/bin/python manage.py %s' % (
                    app,
                    cmd
                )
            )
