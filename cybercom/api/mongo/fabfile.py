from fabric.api import *
from fabric.contrib.files import exists
from fabric.colors import red

env.sitename = 'mongo'
env.mongo_host = 'fire.rccc.ou.edu'
env.psql_host = 'fire.rccc.ou.edu'
env.path = '/scratch/www/wsgi_sites/%(sitename)s' % env
env.virtpy = '/scratch/www/wsgi_sites/%(sitename)s/virtpy' % env 
env.log_path = '/scratch/www/wsgi_sites/%(sitename)s/log' % env
env.apache_config_path = '/etc/httpd/conf.d/%(sitename)s' % env
env.python = 'python2.6'

 
def staging():
    """
    Work on staging environment
    """
    env.settings = 'testing'
    env.hosts = ['fire.rccc.ou.edu']

def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = ['fire.rccc.ou.edu']
    
def setup():
    """ 
    Setup directories and copy everything but virtual environment to server,
        then install virtual environment based on requirements.txt
    """
    setup_directories()
    copy_working_dir()
    setup_virtualenv()
    install_requirements()

def deploy():
    copy_working_dir()

def setup_directories():
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(log_path)s' % env)
    run('mkdir -p %(virtpy)s' % env)

def setup_virtualenv():
    run('virtualenv -p %(python)s --no-site-packages %(virtpy)s' % env)

def copy_working_dir():
    local('tar --exclude virtpy -czf /tmp/deploy_%(sitename)s.tgz .' % env)
    put('/tmp/deploy_%(sitename)s.tgz' % env, '%(path)s/deploy_%(sitename)s.tgz' % env)
    run('cd %(path)s; tar -xf deploy_%(sitename)s.tgz; rm deploy_%(sitename)s.tgz' % env)
    local('rm /tmp/deploy_%(sitename)s.tgz' % env)

def install_requirements():
    check = exists('%(path)s/requirements.txt' % env)
    if check:
        run('source %(virtpy)s/bin/activate; pip install -E %(virtpy)s -r %(path)s/requirements.txt' % env)
    else:
        print red("Can't find requirements.txt!")

