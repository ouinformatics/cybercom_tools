import getAMF as ga
import cx_Oracle as db
import shlex, sys
import datetime

#filename = 'C:/App/Database/Scripts/ameriflux_2011_01_10abc.txt'
#locIDFilename = 'C:/App/Database/Scripts/AMout1.out'
filename = 'C:/App/Database/Scripts/amf_sitebyname_11_01_13.dat'
locIDFilename = 'C:/App/Database/Scripts/amf_sitebyid_11_01_13.dat'
ga.loadAMF(filename,locIDFilename,'cdiac.ornl.gov')

