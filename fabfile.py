#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import project

import os

# Fab settings
env.hosts = ['igelware-group']
env.use_ssh_config = True

PROJECT = "PROJECT"
APPS = {
    "PROJECT": {
        "primary_domain": None,
        "redirect_domains": [
        ],
    }
}


CMSHOSTING_REMOTE = "/var/www/cmshosting"
CMSHOSTING_LOCAL = "/home/sbraun/Projects/cmshosting"
BASEDIR = os.path.dirname( env.real_fabfile )

DEPLOY_PATH = "%s/projects/%s" % (CMSHOSTING_REMOTE, PROJECT)
DEPLOY_NGINX = "%s/configs/nginx/%s-%%s.conf" % (CMSHOSTING_REMOTE, PROJECT)

PYTHON = "virtenv/bin/python"
DJANGO = "virtenv/bin/django-admin.py"
MANAGE = "manage.py"

# used as template variables for uploaded files
KWARGS = {
    'project': PROJECT,
    'user': env.user,
    'basedir': DEPLOY_PATH,
    'app': None,
}

# overwrite this methods ======================================================

COPY_DB_EXCLUDE = [
    '', # keep me, so we can use join
    'contenttypes', # use natural keys instead
    'auth.permission', # use natural keys instead
    'sessions', # no need for this data
    'admin.logentry', # no need for this data
    'south', # FIXME uncomment if using south
    'easy_thumbnails', # FIXME uncomment if using easy_thumbnails
   #'djcelery', # FIXME uncomment if using celery
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
            local('yui-compressor --type css -o media/css/%s-bootstrap.min.css bootstrap.css' % app)
        local('rm bootstrap.css')

@task
def js():
    """
    compiles/copies js
    """
    with lcd(BASEDIR):
        for app in APPS:
            local('cp js/jquery.min.js media/js/')
            local('cp submodules/bootstrap/dist/js/bootstrap.min.js media/js/')


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
                print "========= DONE =========="

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
def install():
    """
    installs the project locally
    """
    with lcd(BASEDIR):
        local('rm -f %s/database.sqlite' % PROJECT)
        migrate(remote=False, first=True)

        if files.exists(DEPLOY_PATH):
            copy_db()
        elif os.path.exists('fixtures_live.json'):
            managepy('loaddata fixtures_live.json', False)
        elif os.path.exists('fixtures_initial.json'):
            managepy('loaddata fixtures_initial.json', False)

        project.rsync_project(
            remote_dir=DEPLOY_PATH + '/media/',
            local_dir=BASEDIR + '/media',
            upload=False,
        )

        managepy('collectstatic --noinput', False)

@task
def copy_db():
    '''
    Copy the production DB locally for testing.
    '''
    with lcd(BASEDIR):
        managepy('dumpdata -n --indent=1 %s > %s/dumpdata.json' % (' -e '.join(COPY_DB_EXCLUDE), DEPLOY_PATH))
        get('%s/dumpdata.json' % DEPLOY_PATH, 'fixtures_live.json')
        run('rm %s/dumpdata.json' % DEPLOY_PATH)
        managepy('loaddata fixtures_live.json', False)

@task
def start():
    """
    starts the project locally
    """
    managepy('runserver 8000', False)

@task
def shell():
    """
    starts a shell locally
    """
    managepy('shell', False)

@task
def test():
    """
    starts a test locally
    """
    managepy('test', False)


# production (fabric-public methods) ==========================================
#       files.upload_template('remote_settings.py', PROJECT+'/local_settings.py', context=KWARGS, use_jinja=True)


@task
def update_nginx():
    pass


@task
def install_remote():
    if files.exists(DEPLOY_PATH):
        puts("%s already exists on remote" % DEPLOY_PATH)
        exit(1)
    git = local("git remote -v | grep origin | grep push | awk '{ print $2 }'", capture=True)
    run('git clone %s %s' % (git, DEPLOY_PATH))
    for app in APPS:
        files.upload_template('remote_settings.py', DEPLOY_PATH + '/' + app + '/local_settings.py', context=KWARGS, use_jinja=True)

    managepy('syncdb --noinput --all', remote)
    managepy('migrate --fake', remote)


@task
def upgrade_remote():
    if not files.exists(DEPLOY_PATH):
        puts("%s does not exist on remote" % DEPLOY_PATH)
        exit(1)


@task
def deploy():
    """
    Update code on the servers, no nginx changes!
    """
    if not files.exists(DEPLOY_PATH):
        puts("%s does not exist on remote" % DEPLOY_PATH)
        exit(1)
    local("git push")
    run('git pull')
    managepy('collectstatic --noinput')
    managepy('syncdb --noinput')
    managepy('migrate')
    run('touch %s/configs/uwsgi.ini')


#   # check_sudo()
#   if not files.exists(DEPLOY_PATH):
#       puts("Cloning %s from git repository" % PROJECT)
#       git = local("git remote -v | grep origin | grep push | awk '{ print $2 }'", capture=True)
#       print(git)
#   else:
#       local("git push")
#       run('git pull')
#       update_nginx()

#   exit(1)

    """
    install
    L: git push
    R: git clone git@igelware.de:griba
    L: scp remote_settings.py igelware-group:/var/www/cmshosting/projects/griba/griba/local_settings.py
    R: /var/www/cmshosting/virtenv/bin/python manage.py collectstatic --noinput
    R: /var/www/cmshosting/virtenv/bin/python manage.py syncdb --all --noinput
    R: /var/www/cmshosting/virtenv/bin/python manage.py migrate --fake
    R: ln -s /var/www/cmshosting/projects/griba/nginx.conf /var/www/cmshosting/configs/nginx/griba-griba.conf
    R: touch /var/www/cmshosting/configs/uwsgi.ini
    R: sudo service nginx reload
    """

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


def managepy(cmd, remote=True):
    """
    Helper: run a management command remotely.
    """
    if remote:
        with cd(DEPLOY_PATH):
            run('%s/%s %s %s' % (CMSHOSTING_REMOTE, PYTHON, MANAGE, cmd))
    else:
        with lcd(BASEDIR):
            local('%s/%s %s %s' % (CMSHOSTING_LOCAL, PYTHON, MANAGE, cmd))


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
