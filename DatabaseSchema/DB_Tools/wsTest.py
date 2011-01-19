import syncWS as sync
import cx_Oracle as db
import shlex, sys
import datetime


'''
Test for Ameriflux Data
SiteID,Year(s), Type {TDF_M, TDF_W,TDF_D, TDF_H}, Variables to Return - Optional 
'''
#
#sync.getAMF_SiteID('uS-ha1','1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006','TDF_M','PRECIP,GPP_OR_ANN')

'''
Dumps data held in cache. Keeps Cataloged Index
Requires CAT_ID
'''
#sync.dumpData(1874)
'''
Test for EOMF Data. LAT,LON,Product,Year (Must be pass as sting), Variables to Return - Optional 
'''
sync.getEOMFdata(35.034,-99.8437,'mod09a1','2009,2010','REAL_DATE,SUR_Refl_B03')


'''
def getRows(site,year,type,col):
    sync.getAMF_SiteID(site,year,type,col)
def main(argv = None):
    if argv is None:
        argv = sys.argv
    options = {}
    options.update(siteID=argv[1],mYear=argv[2],Type=argv[3],Columns=argv[4])
    return getRows(options['siteID'], options['mYear'], options['Type'],options['Columns'])

if __name__ == "__main__":
    sys.exit(main())
'''    