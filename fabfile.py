#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files
from fabric.contrib import project

import json
import os


# SETTINGS ====================================================================


PROJECT = "elmnt"

DEPLOY = {
    'dev': {
        'ssh_host': 'elmnt-server',
        'basedir': '/var/www/cmshosting/%s' % PROJECT,
    },
    'prod': {
        'ssh_host': 'djangobmf',
        'basedir': '/var/www/cmshosting/%s' % PROJECT,
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
def init():
    """
    initialize apps
    """
    pass


@task
def export_local_db():
    '''
    Export local database into fixtures_live.json
    '''
    with lcd(BASEDIR):
        managepy_local('dumpdata --natural-foreign --indent=1 %s > fixtures_local.json' % (' -e '.join(COPY_DB_EXCLUDE)))


@task
def start():
    """
    starts the project locally
    """
    managepy_local('runserver 0.0.0.0:8000', toolbar=True)


@task
def test():
    """
    starts a test locally
    """
    managepy_local('test')


@task
def migrate():
    with lcd(BASEDIR):
        managepy_local('migrate --noinput')


@task
def makemigrations(app):
    with lcd(BASEDIR):
        managepy_local('makemigrations %s' % app)


@task
def flush():
    with lcd(BASEDIR):
        managepy_local('flush --noinput')


@task
def loaddata(fixture):
    with lcd(BASEDIR):
        if not os.path.exists('virtenv') and os.path.exists('docker-compose.yml'):
            prefix = "/project/"
        else:
            prefix = ""
    managepy_local('loaddata %s%s.json' % (prefix, fixture))


@task
def install():
    """
    installs the project locally
    """
    with lcd(BASEDIR): 
        migrate()
        flush()
        if os.path.exists('fixtures_live.json'):
            loaddata('fixtures_live')
        else:
            managepy_local('createsuperuser')


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
def push_fixtures(name):
    """
    Copy the DB from local to remote
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    with lcd(BASEDIR):
        tmp = run('mktemp -d')
        put(name, tmp)
        sudo('chown -R %s %s' % (env.CFG["user"], tmp))
        managepy_remote('loaddata %s/%s' % (tmp, name))
        sudo('rm -rf %s' % tmp)


@task
def push_db():
    """
    Copy the DB from local to remote
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
        managepy_remote('flush --noinput')
        managepy_remote('loaddata %s/fixtures_live.json' % tmp)
        sudo('rm -rf %s' % tmp)


@task
def pull_db():
    """
    Copy the DB from remote to local
    """
    if not hasattr(env, 'CFG'):
        puts("You need to load an environment")
        return False

    database = get_database(env.CFG)

    with lcd(BASEDIR):
        if database:
            tmp = sudo('mktemp', user=env.CFG["user"], group=env.CFG["group"])
            sudo(
                'PGPASSWORD="%s" pg_dump -d %s -h %s -p %s -U %s --no-owner --no-acl --no-privileges --no-tablespaces --no-security-labels --clean -E UTF-8 > %s' % (
                    database['PASSWORD'],
                    database['NAME'],
                    database['HOST'],
                    database['PORT'],
                    database['USER'],
                    tmp,
                ),
                user=env.CFG["user"],
                group=env.CFG["group"],
            )
            sudo('chown %s %s' % (env.user, tmp))
            get(tmp, 'pg_database.dump')
            sudo('rm %s' % tmp)
            # TODO install database from dump
            puts('-' * 80)
            puts('(!) You need to run:')
            puts('> docker-compose -f dbshell.yml run --rm dbshell /bin/bash')
            puts('> PGPASSWORD="$POSTGRES_ENV_POSTGRES_PASSWORD" psql -h $POSTGRES_1_PORT_5432_TCP_ADDR -p $POSTGRES_1_PORT_5432_TCP_PORT -U $POSTGRES_ENV_POSTGRES_USER -d postgres -f /project/pg_database.dump')
            puts('-' * 80)
        else:
            tmp = sudo('mktemp', user=env.CFG["user"], group=env.CFG["group"])
            managepy_remote('dumpdata --natural-foreign --indent=1 %s > %s' % (' -e '.join(COPY_DB_EXCLUDE), tmp))
            sudo('chown %s %s' % (env.user, tmp))
            get(tmp, 'fixtures_live.json')
            sudo('rm %s' % tmp)
            install()


@task
def push_media():
    """
    Copy the media from local to remote
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
    Copy the media from remote to local
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
    sudo('salt-call state.sls hosting.cmstemplate')


def get_database(config):
    virt = os.path.join(BASEDIR, 'virtenv')
    comp = os.path.join(BASEDIR, 'docker-compose.yml')
    with lcd(BASEDIR):
        if not os.path.exists(virt) and os.path.exists(comp):
            with cd(config['basedir']):
                with settings(hide('stdout')):
                    database = json.loads(sudo(
                        'python -c "from homepage import settings; import json; print(json.dumps(settings.DATABASES[\'default\']))"',
                        user=config["user"],
                        group=config["group"],
                    ))
            if database.pop('ENGINE', None) == "django.db.backends.postgresql_psycopg2":
                if not database.get('PORT') and database.get('HOST'):
                    database['PORT'] = 5432
                return database
            else:
                return {}
    return {}


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


@task
def update_cmstemplate():
    with lcd(BASEDIR): 
        local('git checkout cmstemplate')
        local('git pull')
        local('git checkout develop')
        local('git merge -m "merge" cmstemplate')
    

def managepy_local(cmd, toolbar=False):
    virt = os.path.join(BASEDIR, 'virtenv')
    comp = os.path.join(BASEDIR, 'docker-compose.yml')
    with lcd(BASEDIR):
        if not os.path.exists(virt) and os.path.exists(comp):
            local('docker-compose run --rm -p 8000:8000 -e DJANGO_DEBUG_TOOLBAR=%s web python manage.py %s' % (1 if toolbar else '""', cmd))
        else:
            local('export DJANGO_DEBUG_TOOLBAR=%s && virtenv/bin/python manage.py %s' % (1 if toolbar else '""', cmd))


def managepy_remote(cmd):
    with cd(env.CFG['basedir']):
        sudo(
            'virtenv/bin/python manage.py %s' % cmd,
            user=env.CFG["user"],
            group=env.CFG["group"],
        )
