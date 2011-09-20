import os
if os.uname()[1] == 'test.cybercommons.org':
    basedir = '/var/www/apps/'
elif os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'

activate_this = basedir + 'dataportal/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import sys
# put the Django project on sys.path
path = '/scratch/www/wsgi_sites'
if path not in sys.path:
    sys.path.append(path)

import site
site.addsitedir(basedir + 'dataportal')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dataportal.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


