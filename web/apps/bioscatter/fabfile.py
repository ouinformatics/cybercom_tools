''' This fabfile is for use with deploying javascript-only applications to the cybercommons '''

from fabric.api import *
from fabric.contrib.files import exists
from fabric.colors import red
import os

env.sitename = os.path.basename(os.getcwd())
env.host = 'static.cybercommons.org'


def testing():
    """
    Work on staging environment
    """
    env.settings = 'testing'
    env.path = '/static/apptest/%(sitename)s' % env
    env.virtpy = '%(path)s/virtpy' % env
    env.log_path = '%(path)s/log' % env
    env.hosts = ['static.cybercommons.org']

def production():
    """
    Work on staging environment
    """
    env.settings = 'production'
    env.path = '/static/app/%(sitename)s' % env
    env.virtpy = '%(path)s/virtpy' % env
    env.log_path = '%(path)s/log' % env
    env.hosts = ['static.cybercommons.org']

def setup_directories():
    run('mkdir -p %(path)s' % env)

def setup():
    setup_directories()
    copy_working_dir()

def deploy():
    copy_working_dir()

def copy_working_dir():
    local('tar --exclude fabfile.py --exclude fabfile.pyc -czf /tmp/deploy_%(sitename)s.tgz .' % env)
    put('/tmp/deploy_%(sitename)s.tgz' % env, '%(path)s/deploy_%(sitename)s.tgz' % env)
    run('cd %(path)s; tar -xf deploy_%(sitename)s.tgz; rm deploy_%(sitename)s.tgz' % env)
    local('rm /tmp/deploy_%(sitename)s.tgz' % env)



