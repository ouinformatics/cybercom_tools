import os
import sys
import site


# Set up virtual environment
site_packages = '/scratch/www/wsgi_sites/flora/project/virtpy/lib/python2.6/site-packages'
site.addsitedir(os.path.abspath(site_packages))

# Add project directory to python path
path = '/scratch/www/wsgi_sites/flora/project'
if path not in sys.path:
    sys.path.append(path)


sys.path.append('/scratch/www/wsgi_sites/flora')


os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
