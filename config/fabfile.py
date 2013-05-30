import yaml
import re
from fabric.api import *
from fabric.colors import magenta, red, green, yellow
from fabric.context_managers import hide,show
config = yaml.load(open('/Users/jduckles/git/cybercom/config/config.yaml','r').read())

def hostgroup(hosttype):
    return [ worker['host'] for worker in config[hosttype] ]

def all_hosts(config):
    if 'host' in config:
        yield config['host']
    for k in config:
        if isinstance(config[k], list):
            for i in config[k]:
                for j in all_hosts(i):
                    yield j

def workers():
    env.hosts = hostgroup('workers')
    env.service = 'celeryd'

def wsgi():
    env.hosts = hostgroup('wsgi')
    env.service = 'httpd'

def mongo():
    env.hosts = hostgroup('mongo')
    env.service = 'mongod'

def static():
    env.hosts = hostgroup('static')
    env.service = 'nginx' 

def varnish():
    env.hosts = hostgroup('varnish')
    env.service = 'varnish'

def memcache():
    pass

def queue():
    env.hosts = hotgroup('queue')
    env.service = 'rabbitmq'

def service(srv):
    with settings(warn_only = True):
        out = sudo('/etc/init.d/%s %s' % (env.service, srv))
        if len(re.findall('running', out)) > 0:
            print green("Service running")
        elif len(re.findall('stopped',out)) > 0:
            print red("Service not running")
        elif len(re.findall('Starting', out)) > 0:
            print green("Service restarted")


def status():
    service('status')

@hosts( list(set([ item for item in all_hosts(config)])) )
def status_all():
    with hide('running','stdout','status'):
        host = magenta(run('hostname'))
    with hide('running','stdout','status'):
        out = green(run('uptime'))
    print "%s - %s" % (host.ljust(40), out)

def start():
    service('start')

def stop():
    service('stop')

def restart():
    service('restart')
 
def uptime():
    output = run('uptime')
    print magenta(output)

