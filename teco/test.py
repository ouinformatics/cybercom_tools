#!/usr/bin/python26
'''
Created on Nov 22, 2010

@author: stac3294
'''
import db_push as db1
import sys

newSEQ = sys.argv[1]
CFILE = sys.argv[2]
H2OFILE = sys.argv[3]
POOLFILE = sys.argv[4]

f1 = open(CFILE,'r')#objFile
db1.TECO2DB(newSEQ,'C_FILE',f1)
f2 = open(H2OFILE,'r')#objFile
db1.TECO2DB(newSEQ,'H2O_FILE',f2)
f3 = open(POOLFILE,'r')#objFile
db1.TECO2DB(newSEQ,'POOL_FILE',f3)
