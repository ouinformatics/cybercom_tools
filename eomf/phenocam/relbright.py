#!/usr/bin/env python
import sys
import Image
import numpy
import json
import re
from datetime import datetime

def relbright(fname):
    fname=sys.argv[1]
    pat = re.compile(r'[0-9]{4}-[0-9]{4}-[0-9]{6}')
    timestr = pat.findall(fname)[0]
    timeformat="%Y-%m%d-%H%M%S"
    isodate = datetime.strptime(timestr,timeformat).isoformat()
    keys = ['r','g','b']
    im = Image.open(fname)
    a = numpy.array(im.getdata())
    relbright = a.sum(axis=0)/float(a.sum())
    return {'brightness': dict(zip(keys,relbright))}
