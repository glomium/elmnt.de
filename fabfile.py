#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import project

import os

PROJECT = "elmnt"
APPS = {
    "elmnt": {
        "primary_domain": "www.elmnt.de",
        "redirect_domains": [
            "elmnt.de",
        ],
    }
}

DEPLOY = {
    'local': {
        # False/None/Empty or path to (shared) hosting env
        # if Path the project won't be installed with the cmshosting package
        'cmshosting': False,
        # path to the project
        'project_path': '',
        # ????
        'nginx': "",
        # use sudo
        'use_sudo': True,
        # ssh to this host - use None or False for local installations
        'ssh_host': None,
        # overwrite virtualenv executable
        'virtualenv': 'virtenv',
        'local': True,
    },
    'dev': {
        # False/None/Empty or path to (shared) hosting env
        # if Path the project won't be installed with the cmshosting package
        'cmshosting': False,
        # path to the project
        'project_path': "%(cmshosting)s/projects/%(project)s",
        'nginx': "",
        'use_sudo': True,
        'ssh_host': 'igelware-group',
        # overwrite virtualenv executable
        'virtualenv': 'virtenv',
    },
}

# Default env for production
PRODUCTION = None

BASEDIR = os.path.dirname( env.real_fabfile )

@task
def localhost():
    set_env("local")

@task
def dev():
    set_env("dev")

@task
def prod():
    set_env("prod")

# overwrite this methods ======================================================

COPY_DB_EXCLUDE = [
    '', # keep me, so we can use join
    'contenttypes', # use natural keys instead
    'auth.permission', # use natural keys instead
    'sessions', # no need for this data
    'admin.logentry', # no need for this data
    'easy_thumbnails', # FIXME uncomment if using easy_thumbnails
]

@task
def static():
    """
    complies/copies static files
    """
    js()
    css()
    with lcd(BASEDIR):
        for app in APPS:
            local('cp submodules/bootstrap/fonts/glyphicons-halflings-regular* media/fonts/')

@task
def css():
    """
    compiles/copies css
    """
    with lcd(BASEDIR):
        for app in APPS.keys():
            local('lessc less/%s.less > bootstrap.css' % app)
            local('yui-compressor --type css -o media/css/%s.min.css bootstrap.css' % app)
        local('rm bootstrap.css')

@task
def js():
    """
    compiles/copies js
    """
    with lcd(BASEDIR):
        local('cp submodules/bootstrap/dist/js/bootstrap.min.js media/js/')
        for app in APPS:
            local('yui-compressor --type js -o media/js/%s.min.js js/%s.js' % (app, app))


# development (fabric-public methods) =========================================

def parse_deploy(config):
    # select the current key from settings
    template = DEPLOY.get(config)
    template['project'] = PROJECT

    deploy = {}

    # use cmshosting and set paths to environment
    if not template.get('cmshosting', False):
        deploy['use_cmshosting'] = False
        deploy['cmshosting'] = template['project_path'] % template
    else:
        deploy['use_cmshosting'] = True
        deploy['cmshosting'] = template['cmshosting'] % template

    # update and parse the project path
    deploy['project_path'] = template['project_path'] % template

    deploy['basedir'] = template.get('basedir', BASEDIR)

    deploy['virtenv'] = template.get('virtenv', '%s/virtenv' % BASEDIR)

    deploy['python'] = template.get('python', 'bin/python')
    deploy['django'] = template.get('django', 'bin/django-admin.py')
    deploy['manage'] = template.get('manage', 'manage.py')

    # use current working directory
    deploy['local'] = template.get('local', False)

    deploy['use_sudo'] = template.get('use_sudo', False)
    deploy['settings'] = template.get(
        'settings',
        'settings_%s_%%s.py' % config
    )
    deploy['ssh_host'] = template.get('ssh_host', None) or 'localhost'
    deploy['virtualenv'] = template.get('virtualenv', 'virtualenv')

    return deploy

def set_env(e):
    setattr(env, 'CFG', parse_deploy(e))

    env.hosts = [env.CFG['ssh_host'],]
    env.use_ssh_config = True

    setattr(env, 'KWARGS', {
        'project': PROJECT,
        'user': env.user,
        'basedir': env.CFG['project_path'],
        'app': None,
        'cmshosting': env.CFG['cmshosting'],
        'use_cmshosting': env.CFG['use_cmshosting'],
    })

# development (fabric-public methods) =========================================

@task
def watchstatic():
    static()
    import pyinotify
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

            if not os.path.exists('less/%s.less' % app):
                local("touch less/%s.less" % app)

            if not os.path.exists('js/%s.js' % app):
                local("touch js/%s.js" % app)


## UNTESTED BELOW THIS LINE ===========================================================================================

@task
def install():
    """
    installs the project locally
    """
    if not hasattr(env, 'CFG'):
        localhost()

    with lcd(BASEDIR): 
        local('rm -f %s/database.sqlite' % PROJECT)
        managepy('migrate --noinput')

        copy_db()
        copy_media()

        if os.path.exists('fixtures_live.json'):
            managepy('loaddata fixtures_live.json')
        else:
            managepy('createsuperuser')

        managepy('collectstatic --noinput')


@task
def copy_db():
    '''
    Copy the production DB locally for testing.
    '''
    if not PRODUCTION and not env.CFG['local']:
        puts("SKIPPING copy_db: Production not set or not inside a local env")
        return False

#   with lcd(BASEDIR):
#       managepy('dumpdata -n --indent=1 %s > %s/dumpdata.json' % (' -e '.join(COPY_DB_EXCLUDE), DEPLOY_PATH))
#       get('%s/dumpdata.json' % DEPLOY_PATH, 'fixtures_live.json')
#       run('rm %s/dumpdata.json' % DEPLOY_PATH)
#       managepy('loaddata fixtures_live.json', False)


@task
def copy_media():
    '''
    Copy the production media locally
    '''
    if not PRODUCTION and not env.CFG['local']:
        puts("SKIPPING copy_media: Production not set or not inside a local env")
        return False

#   project.rsync_project(
#       remote_dir=DEPLOY_PATH + '/media/',
#       local_dir=BASEDIR + '/media',
#       upload=False,
#   )


@task
def export_local_db():
    '''
    '''
    if not hasattr(env, 'CFG'):
        localhost()

    if not env.CFG['local']:
        puts("ERROR export_local_db: Not inside a local env")
        exit(1)

    with lcd(BASEDIR):
        managepy('dumpdata -n --indent=1 %s > fixtures_live.json' % (' -e '.join(COPY_DB_EXCLUDE)))


@task
def start(app=None):
    """
    starts the project locally
    """
    if not hasattr(env, 'CFG'):
        localhost()

    if not app:
        app = APPS.keys()[0]

    if env.CFG['local']:
        with lcd(env.CFG['basedir']):
            local('%s/bin/uwsgi uwsgi.ini --http=0.0.0.0:8000' % env.CFG['virtenv'])


@task
def shell(app=None):
    """
    starts a shell locally
    """
    if not hasattr(env, 'CFG'):
        localhost()
    managepy('shell', app)


@task
def test(app=None):
    """
    starts a test locally
    """
    if not hasattr(env, 'CFG'):
        localhost()
    managepy('test', app)


# production (fabric-public methods) ==========================================


@task
def update_nginx():
    """
    install
    R: ln -s /var/www/cmshosting/projects/griba/nginx.conf /var/www/cmshosting/configs/nginx/griba-griba.conf
    R: touch /var/www/cmshosting/configs/uwsgi.ini
    R: sudo service nginx reload
    """
    check_sudo()


@task
def install_remote():
    """
    install the project on the remote server
    """
    check_sudo()

    if files.exists(DEPLOY_INFO['project_path']):
        puts("%s already exists on remote" % DEPLOY_INFO['project_path'])
        exit(1)

    git = local("git remote -v | grep origin | grep push | awk '{ print $2 }'", capture=True)
    run('git clone %s %s' % (git, DEPLOY_INFO['project_path']))

    if not DEPLOY_INFO['cms_hosting']:
        # create virtualenv and install requirements
        # TODO
        puts("TODO: create virtualenv and install requirements")
        pass

    upgrade_remote_settings()

    # TODO Do this for every APP
    managepy('syncdb --noinput --all', True)
    managepy('migrate --fake', True)
    managepy('collectstatic --noinput', True)

    update_nginx()


def upgrade_remote_settings():
    for app in APPS:
        files.upload_template(
            DEPLOY_INFO['settings'] % app,
            DEPLOY_INFO['project_path'] + '/' + app + '/local_settings.py',
            context=KWARGS,
            use_jinja=True,
        )


@task
def upgrade_remote():
    if not files.exists(DEPLOY_PATH):
        puts("%s does not exist on remote" % DEPLOY_PATH)
        exit(1)


@task
def fast_deploy():
    """
    Update code on the servers, no nginx+uwsgi changes!
    """
    if not files.exists(DEPLOY_INFO['project_path']):
        puts("%s already exists on remote" % DEPLOY_INFO['project_path'])
        exit(1)
    local("git push")
    with cd(DEPLOY_INFO['project_path']):
        run('git pull')


@task
def deploy():
    """
    Update code on the servers, no nginx changes!
    """
    fast_deploy()

    upgrade_remote_settings()

    with cd(DEPLOY_PATH):
        managepy('collectstatic --noinput')
        managepy('syncdb --noinput')
        managepy('migrate')

    run('touch %s/configs/uwsgi.ini' % CMSHOSTING_REMOTE)


#   # check_sudo()
#   if not files.exists(DEPLOY_PATH):
#       puts("Cloning %s from git repository" % PROJECT)
#       git = local("git remote -v | grep origin | grep push | awk '{ print $2 }'", capture=True)
#       puts(git)
#   else:
#       local("git push")
#       run('git pull')
#       update_nginx()

#   exit(1)


    """
    update
    L: git push
    R: git pull
    R: /var/www/cmshosting/virtenv/bin/python manage.py collectstatic --noinput
    R: /var/www/cmshosting/virtenv/bin/python manage.py syncdb --noinput
    R: /var/www/cmshosting/virtenv/bin/python manage.py migrate 
    R: touch /var/www/cmshosting/configs/uwsgi.ini
    """

#   if not files.exists(DEPLOY_PATH):
#       puts("Cloning %s from git repository" % PROJECT)
#       git = local("git remote -v | grep origin | grep push | awk '{ print $2 }'", capture=True)
#       run('git clone %s %s' % (git, DEPLOY_PATH))
#       first = True
#   else:
#       local("git push")
#       first = False

#   if not files.exists(DEPLOY_PATH+VIRTENV):
#       recreate = True

#   with cd(DEPLOY_PATH):
#       puts("Deploying project %s" % PROJECT)
#       run('git pull')

#       # update configurations
#       KWARGS = {
#           'project': PROJECT,
#           'prefix': PREFIX,
#           'user': env.user,
#           'basedir': DEPLOY_PATH,
#           'virtenv': VIRTENV,
#       }

#       files.upload_template('remote_settings.py', PROJECT+'/local_settings.py', context=KWARGS, use_jinja=True)
#       files.upload_template('templates/'+CFG_NGINX, CFG_NGINX, context=KWARGS, use_jinja=True)
#       files.upload_template('templates/'+CFG_UWSGI, CFG_UWSGI, context=KWARGS, use_jinja=True)
#       files.upload_template('templates/'+CFG_SUPERVISOR, CFG_SUPERVISOR, context=KWARGS, use_jinja=True)

#       sudo('ln -fs %s%s %s' % (DEPLOY_PATH, CFG_NGINX, DEPLOY_NGINX))
#       sudo('ln -fs %s%s %s' % (DEPLOY_PATH, CFG_SUPERVISOR, DEPLOY_SUPERVISOR))

#       # change group to www-data
#       sudo('chgrp -f www-data .')
#       sudo('chgrp -fR www-data %s' % PROJECT)

#       if recreate:
#           run('tox -re production')
#           local("%s/bin/pip freeze > freeze.txt" % VIRTENV)

#   migrate(first=first)

#   with lcd(BASEDIR):
#       with cd(DEPLOY_PATH):
#           if first and (os.path.exists('fixtures_initial.json') or os.path.exists('fixtures_live.json')):
#               if os.path.exists('fixtures_live.json'):
#                   files.upload_template('fixtures_live.json', 'fixtures_tmpupload.json', use_jinja=False, backup=False)
#               else:
#                   files.upload_template('fixtures_initial.json', 'fixtures_tmpupload.json', use_jinja=False, backup=False)
#               managepy('loaddata fixtures_tmpupload.json')
#               run('rm -f fixtures_tmpupload.json')

#   collectstatic()
#   supervisor('update')
#   supervisor('restart %s-%s:' % (PREFIX, PROJECT))
#   nginx("reload")
#   memcached("restart")


# server management (fabric-private methods) ==================================


def check_sudo():
    """
    check if user has sudo permissions
    """
    if DEPLOY_INFO['use_sudo']:
        sudo("uname -a")


def nginx(cmd):
    """
    Manage the nginx service. For example, `fab nginx:restart`.
    """
    sudo('/etc/init.d/nginx %s' % cmd)


def memcached(cmd):
    """
    Manage the memcached service. For example, `fab memcached:restart`.
    """
    return None
    sudo('/etc/init.d/memcached %s' % cmd)


def managepy(cmd, app=None):
    """
    Helper: run a management command remotely.
    """
    if not app:
        app = APPS.keys()[0]

    if env.CFG['local']:
        with lcd(env.CFG['basedir']):
            local(
                'export DJANGO_SETTINGS_MODULE=%s.settings && %s/%s %s %s' % (
                    app,
                    env.CFG['virtenv'],
                    env.CFG['python'],
                    env.CFG['manage'],
                    cmd
                )
            )
    else:
        with cd(env.CFG['basedir']):
            run(
                'export DJANGO_SETTINGS_MODULE=%s.settings && %s/%s %s %s' % (
                    app,
                    env.CFG['virtenv'],
                    env.CFG['python'],
                    env.CFG['manage'],
                    cmd
                )
            )


def collectstatic(remote=True):
    """
    Run django collectstatic
    """
    managepy('collectstatic --noinput', remote)


def migrate(remote=True, first=False):
    with lcd(BASEDIR):
        migrations = local("%s/%s -c 'from django import VERSION; print((VERSION[0] == 1 and VERSION[1] >= 7) or (VERSION[0] > 1))'" % (CMSHOSTING_LOCAL, PYTHON), capture=True)

    if migrations == "True":
        managepy('migrate --noinput', remote)

    elif check_installed_app('south'):
        if first:
            managepy('syncdb --noinput --all', remote)
            managepy('migrate --fake', remote)
        else:
            managepy('syncdb --noinput', remote)
            managepy('migrate', remote)
    else:
        managepy('syncdb --noinput', remote)


def check_installed_app(app):
    with lcd(BASEDIR):
        return bool(local("%s/%s -c 'from %s.settings import INSTALLED_APPS; print(\"%s\" in INSTALLED_APPS)'" % (CMSHOSTING_LOCAL, PYTHON, PROJECT, app), capture=True))
    return False


def supervisor(cmd):
    """
    Manage supervisord
    """
    sudo('supervisorctl %s' % cmd)
