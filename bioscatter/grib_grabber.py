import urllib2
from subprocess import Popen, PIPE
import shlex

toget =[    
    ['PRES','surface'],
    ['PRES','max wind'],
    ['UGRD','max wind'],
    ['VGRD','max wind'],
    ['CRAIN','surface'],
    ['CFRZR','surface'],
    ['CICEP','surface'],
    ['CSNOW','surface'],
    ['VIS','surface'],
    ['TMP','surface'],
    ['TMP','100 mb'],
    ['TMP','200 mb'],
    ['TMP','300 mb'],
    ['TMP','400 mb'],
    ['TMP','500 mb'],
    ['TMP','600 mb'],
    ['UGRD','100 mb'],
    ['UGRD','200 mb'],
    ['UGRD','300 mb'],
    ['UGRD','400 mb'],
    ['UGRD','500 mb'],
    ['UGRD','600 mb'],
    ['VGRD','100 mb'],
    ['VGRD','200 mb'],
    ['VGRD','300 mb'],
    ['VGRD','400 mb'],
    ['VGRD','500 mb'],
    ['VGRD','600 mb'],
    ['RH','100 mb'],
    ['RH','200 mb'],
    ['RH','300 mb'],
    ['RH','400 mb'],
    ['RH','500 mb'],
    ['RH','600 mb'],
    ['VVEL','100 mb'],
    ['VVEL','200 mb'],
    ['VVEL','300 mb'],
    ['VVEL','400 mb'],
    ['VVEL','500 mb'],
    ['VVEL','600 mb']
]


def getindex(url):
    try:
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
    except:
        print "Does the URL exist?"
    return [ line.strip().split(':') for line in f.readlines() ]

def computerange(lyrindex):
    for i in range(len(lyrindex)):
        if i != len(lyrindex) - 1:
            lyrindex[i].append( 'range=%s-%s' %( lyrindex[i][1], int(lyrindex[i+1][1]) - 1) )
        else:
            lyrindex[-1].append( 'range=%s' % ( lyrindex[-1][1] ) )
    return lyrindex

def selectlayers(lyrindex,selection):
    return [ [item[2].replace('D=','') ,item[3],item[4],item[-1].replace('range=','') ] 
                for item in lyrindex if [item[3],item[4]] in selection ]

def curlstrings(selections):
    strings = []
    for date, layer, level, getrange in selections:
        level = level.replace(' ','_')
        date = date.replace('d=','')
        strings.append('/usr/bin/curl -r %s "%s" -o %s_%s_%s.grb' %( getrange, url, date, layer, level))
    return strings

def runall(commands):
    for com in commands:
        print "Getting...%s" % com
        p = Popen( shlex.split(com), stdout=PIPE, stderr=PIPE)
        p.wait()

def getlayers(url,layers):
    req = urllib2.Request(url)
    for layer in layers:
        try:
            start,stop = layer[-1].split('-')
            req.headers['Range'] = 'bytes=%s-%s' % (start, stop)
        except:
            start = layer[9].split('=')[1]
            req.headers['Range'] = 'bytes=%s' % (start)
        fi = urllib2.urlopen(req)
        # This shows you the *actual* bytes that have been downloaded.
        fo = open('foo.grb', 'w')
        fo.write(f.read())
        show_range = f.headers.get('Content-Range')
        print(show_range)

if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    layers = selectlayers(computerange(getindex(url)), toget)
    url = url.replace('.inv','.grb2')
    runall(curlstrings(layers))
    

