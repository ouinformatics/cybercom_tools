#!/usr/bin/env python2.6 

from subprocess import Popen, PIPE 
from twisted.web import xmlrpc, server
from datetime import timedelta, datetime
from zipfile import ZipFile
from StringIO import StringIO
import os


class Extract(xmlrpc.XMLRPC):
    ''' Extract radar products '''
    def singleExtract(self, product, lat, lon, radius, time):
        if product = 'unqc_cref':
            call_string = ['/home/jduckles/cybercom/bioscatter/simp_extract', product, lat, lon, radius, time]
            p = Popen( call_string , stdout=PIPE, stderr=PIPE)
            out = p.communicate()[0].strip()
            return out
        elif product = 'RUC':
            pass # call RUC grabs

    def zip_files(self, files):
        ''' Takes a list of file locations and returns a zipfile with directories stripped ''' 
        inMemoryOutputFile = StringIO()
        zipFile = ZipFile(inMemoryOutputFile, 'w')
        for filename in files:
            zipFile.writestr(os.path.basename(filename), open(filename, 'r').read() )
        zipFile.close()
        inMemoryOutputFile.seek(0)
        return inMemoryOutputFile
            
    def date_range(self, start_datetime, end_datetime):
        ''' Generator for datetime_ranges at 5 minute intervals '''
        d = start_datetime
        delta = timedelta(minutes=5)
        while d <= end_datetime:
            yield d.strftime('%Y%m%d.%H%M%S')
            d += delta
               
    def xmlrpc_extractTimestep(self, product, lat, lon, radius, time):
        ''' Extract a single timestep tiffs from a single location with a given radius 
                Example:
                >>> extractTimestep( 'unqc_cref', 33.00, -96.60, 1, '20100705.105000')
        '''
        makezip=True
        if makezip:
            # Return as zipfile containing timsteps
            return self.zip_files(self.singleExtract(product, lat, lon, radius, time))
        else:
            # Return as file locations
            return self.singleExtract(product, lat, lon, radius, time) 
    xmlrpc_extractTimestep.signature = [ ['base64', 'string', 'double', 'double', 'double', 'string'] ]
 
    def xmlrpc_extractTimeseries(self, product, lat, lon, radius, start, stop):
        ''' Extract as timeseries of tifs from single location with a given radius 
                Example:
                >>> extractTimeseries( 'unqc_cref', 33.00, -96.60, 1, '20100705.105000', '20100705.123000')                
        ''' 
        outlist = []
        datetime.strptime( start, '%Y%m%d.%H%M%S')
        timefmt = '%Y%m%d.%H%M%S'
        for time in self.date_range(  datetime.strptime( start, timefmt), datetime.strptime(stop, timefmt) ):
            outlist.append(self.singleExtract( product, lat, lon, radius, time ))
        makezip=True
        if makezip:
            return xmlrpc.Binary(self.zip_files(outlist).read())
        else:
            return outlist
    xmlrpc_extractTimeseries.signature = [ ['base64','string', 'double', 'double', 'double', 'string', 'string'], ]
        

if __name__ == '__main__':
    from twisted.internet import reactor
    r = Extract()
    xmlrpc.addIntrospection(r)
    reactor.listenTCP(8989, server.Site(r))
    reactor.run()



