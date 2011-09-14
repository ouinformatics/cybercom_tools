from fabric.api import *
from fabric.contrib.files import exists, append, comment
from fabric.colors import red
import os 

env.sitename = os.path.basename(os.getcwd())
env.mongo_host = 'fire.rccc.ou.edu'
env.psql_host = 'fire.rccc.ou.edu'
env.apache_config = '/etc/httpd/conf.d/%(sitename)s.conf' % env
env.python = '/usr/bin/python2.6'

 
def testing():
    """
    Work on staging environment
    """
    env.settings = 'testing'
    env.path = '/var/www/apps/%(sitename)s' % env
    env.virtpy = '%(path)s/virtpy' % env
    env.log_path = '%(path)s/log' % env
    env.hosts = ['test.cybercommons.org']

def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.path = '/scratch/www/wsgi_sites/%(sitename)s' % env
    env.virtpy = '%(path)s/virtpy' % env
    env.log_path = '%(path)s/log' % env
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
    apache_config()
    bounce_apache()

def deploy():
    copy_working_dir()
    bounce_apache()

def setup_directories():
    if not exists('%(path)s' % env):
        run('mkdir -p %(path)s' % env)
        run('mkdir -p %(log_path)s' % env)
        run('mkdir -p %(virtpy)s' % env)


def virtualenv(command):
    with cd(env.virtpy):
        run('source %(virtpy)s/bin/activate' % env + '&&' + command)

def setup_virtualenv():
    run('virtualenv -p %(python)s --no-site-packages %(virtpy)s' % env)

def bounce_apache():
    """ Restart the apache web server """
    sudo('/etc/init.d/httpd restart')

def apache_config():
    # check if apache config lines exist in old wsgi_sites.conf and comment if found
    comment('/etc/httpd/conf.d/wsgi_sites.conf', r'^WSGIScriptAlias /%(sitename)s .*$' % env, use_sudo=True)
    if os.path.isfile('/%(sitename)s %(path)s/%(sitename)s.wsgi' % env):
        confline = 'WSGIScriptAlias /%(sitename)s %(path)s/%(sitename)s.wsgi' %env
        append('%(apache_config)s' % env, confline, use_sudo=True)
    else:
        red("Can't find %(sitename)s.wsgi file" % env)

def copy_working_dir():
    local('tar --exclude virtpy -czf /tmp/deploy_%(sitename)s.tgz .' % env)
    put('/tmp/deploy_%(sitename)s.tgz' % env, '%(path)s/deploy_%(sitename)s.tgz' % env)
    run('cd %(path)s; tar -xf deploy_%(sitename)s.tgz; rm deploy_%(sitename)s.tgz' % env)
    local('rm /tmp/deploy_%(sitename)s.tgz' % env)

def install_requirements():
    check = exists('%(path)s/requirements.txt' % env)
    if check:
        virtualenv('pip install -E %(virtpy)s -r %(path)s/requirements.txt' % env)
    else:
        print red("Can't find requirements.txt!")


