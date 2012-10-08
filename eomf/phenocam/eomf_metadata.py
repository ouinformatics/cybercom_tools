#!/home/jduckles/bin/python
import os, re, subprocess, shlex
from datetime import datetime
import json
import hashlib
from relbright import relbright

def exif(fname):
    p = subprocess.Popen(shlex.split('exiftool -j %s' % fname), stdout=subprocess.PIPE)
    return json.loads(p.communicate()[0])

def md5(fname):
    return hashlib.md5(open(fname).read()).hexdigest()

def ls(dir):
    return os.listdir(dir)

def asisoformat(string, datepart, format):
    """ Example: asisoformat('Elreno-2012-0710-133001.jpg', '[0-9]{4}-[0-9]{4}-[0-9]{6}', '%Y-%m%d-%H%M%S') """
    return datetime.strptime( re.search(datepart, string).group(), format).isoformat()

def phenocam(fname):
    md = {}
    md['date'] = asisoformat(fname, '[0-9]{4}-[0-9]{4}-[0-9]{6}', '%Y-%m%d-%H%M%S')
    md['filename'] = os.path.abspath(fname)
    md['host'] = os.uname()[1]
    md['site'] = os.path.basename(fname.split('-')[0])
    md['exif'] = exif(fname)
    md['url'] = 'http://static.cybercommons.org/phenocam/%s/%s' % (md['site'],os.path.basename(fname))
    md['size'] = os.path.getsize(fname)
    md['md5'] = md5(fname)
    md.update(relbright(fname))
    return json.dumps({'date_keys': ["date"], 'database':'eomf_phenocam', 'collection': 'data', 'data': md })

        
if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    print phenocam(fname)

