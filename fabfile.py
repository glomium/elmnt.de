#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import project

import os


# SETTINGS ====================================================================


PROJECT = "FIXME"

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

SUBMODULES = {
}

# env for production (disables push for this env)
PRODUCTION = 'prod'

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
def static(bower=True):
    """
    complies and copies static files
    """
    if bower:
        local('bower update')
    local('grunt')
    with lcd(BASEDIR):
        local('cp bower_components/bootstrap/fonts/glyphicons-halflings-regular* media/fonts/')
        local('cp bower_components/c3/c3.min.css media/css/')
        local('cp bower_components/c3/c3.min.js media/js/')
        local('cp bower_components/d3/d3.min.js media/js/')
        local('cp bower_components/jquery/dist/jquery.min.js media/js/')
        local('cp bower_components/jquery/dist/jquery.min.map media/js/')


@task
def init():
    """
    initialize apps
    """
    pass
#   with lcd(BASEDIR):
#       if not os.path.exists("media"):
#           local("mkdir media")
#           local("mkdir media/js")
#           local("mkdir media/css")
#           local("mkdir media/fonts")
#       if not os.path.exists("static"):
#           local("mkdir static")
#           if not os.path.exists(app) and not os.path.isdir(app):
#               if not os.path.exists("project_template"):
#                   local("git checkout project_template -- project_template")
#               local("mv project_template %s" % app)
#               local("git rm -r project_template")
#               local("sed -i 's/{{ APP }}/%s/g' %s/settings.py" % (app, app))
#               local("sed -i 's/{{ APP }}/%s/g' %s/wsgi.py" % (app, app))



@task
def export_local_db():
    '''
    Export local database into fixtures_live.json
    '''
    with lcd(BASEDIR):
        managepy('dumpdata -n --indent=1 %s > fixtures_local.json' % (' -e '.join(COPY_DB_EXCLUDE)))


@task
def start():
    """
    starts the project locally
    """
    managepy('runserver 0.0.0.0:8000')


@task
def shell(app):
    """
    starts a shell locally
    """
    managepy('shell')


@task
def test(app):
    """
    starts a test locally
    """
    managepy('test')


@task
def install():
    """
    installs the project locally
    """
    with lcd(BASEDIR): 
        local('rm -f database.sqlite')
        managepy('migrate --noinput', app)

        pull_db()
        pull_media()

        if os.path.exists('fixtures_live.json'):
            managepy('loaddata fixtures_live.json')
        else:
            managepy('createsuperuser')

        managepy('collectstatic --noinput')


@task
def update_submodules(init=False):
    '''
    '''
    with lcd(BASEDIR):
        for name, git in SUBMODULES.iteritems():
            repo, branch = git.split("#")
            if os.path.exists('modules/%s' % name) and not init:
                local("git subtree pull --prefix modules/%s %s %s --squash" % (name, repo, branch))
            elif not os.path.exists('modules/%s' % name):
                repo, branch = git.split("#")
                local("git subtree add --prefix modules/%s %s %s --squash" % (name, repo, branch))


@task
def init_submodules():
    '''
    '''
    update_submodules(init=True)


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
        sudo('chown %s %s' % (env.user, tmp))
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

    tmp = sudo('mktemp -d', user=env.user)
    sudo('cp -a %s %s' % (env.CFG['basedir'] + '/media/', tmp))
    sudo('chown -R %s %s' % (env.user, tmp))

    project.rsync_project(
        remote_dir=tmp + '/media',
        local_dir=BASEDIR + '/media/',
        upload=True,
        delete=True,
    )
    sudo('chown -R %s:%s %s' % (env.CFG["user"], env.CFG["group"], tmp))
    sudo('rm -rf %s' % env.CFG['basedir'] + '/media/')
    sudo('mv %s %s' % (tmp + '/media/', env.CFG['basedir']))
    sudo('rm -rf %s' % tmp)


@task
def pull_media():
    """
    Copy the production media from remote to local
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    tmp = sudo('mktemp -d', user=env.CFG["user"], group=env.CFG["group"])
    sudo('cp -a %s %s' % (env.CFG['basedir'] + '/media/', tmp))
    sudo('chown -R %s %s' % (env.user,  tmp))

    project.rsync_project(
        remote_dir=tmp + '/media/',
        local_dir=BASEDIR + '/media',
        upload=False,
    )
    sudo('rm -rf %s' % tmp)

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
    sudo('salt-call state.sls django_projects pillar=\'{"django_projects_active": "%s"}\'' % PROJECT)


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


def managepy(cmd, remote=False):
    """
    Helper: run a management command remotely.
    """

    if remote:
        with cd(env.CFG['basedir']):
            sudo(
                'virtenv/bin/python manage.py %s' % (
                    cmd
                ),
                user=env.CFG["user"],
                group=env.CFG["group"],
            )
    else:
        with lcd(BASEDIR):
            local(
                'export DJANGO_DEBUG_TOOLBAR=True && virtenv/bin/python manage.py %s' % (
                    cmd
                )
            )
