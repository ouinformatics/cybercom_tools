#!/usr/bin/python
import sys
import db_push as dbu
id = sys.argv[1]
file = sys.argv[2]
dbu.INP_2_DB(id,file)
