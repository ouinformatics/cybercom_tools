#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1369248746.111649
__CHEETAH_genTimestamp__ = 'Wed May 22 13:52:26 2013'
__CHEETAH_src__ = 'UNQC_CREF.tmpl'
__CHEETAH_srcLastModified__ = 'Wed May 22 13:52:20 2013'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class UNQC_CREF(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(UNQC_CREF, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<VRTDataset rasterXSize="7001" rasterYSize="3501">
  <SRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;WGS_1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137,298.257223563,AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</SRS>
  <GeoTransform> -1.3000500000000000e+02,  1.0000000000000000e-02,  0.0000000000000000e+00,  5.5005000000000003e+01,  0.0000000000000000e+00, -1.0000000000000000e-02</GeoTransform>
  <VRTRasterBand dataType="Float32" band="1">
    <NoDataValue>-9.99000000000000E+02</NoDataValue>
    <ColorInterp>Gray</ColorInterp>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile1/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 8, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 8, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 8, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 8, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="1501" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="1501" />
      <DstRect xOff="0" yOff="0" xSize="2001" ySize="1501" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile2/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 16, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 16, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 16, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 16, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="1501" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="1501" />
      <DstRect xOff="2000" yOff="0" xSize="2001" ySize="1501" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile3/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 24, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 24, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 24, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 24, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="1001" RasterYSize="1501" DataType="Float32" BlockXSize="1001" BlockYSize="2" />
      <SrcRect xOff="0" yOff="0" xSize="1001" ySize="1501" />
      <DstRect xOff="4000" yOff="0" xSize="1001" ySize="1501" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile4/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 32, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 32, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 32, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 32, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="1501" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="1501" />
      <DstRect xOff="5000" yOff="0" xSize="2001" ySize="1501" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile5/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 40, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 40, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 40, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 40, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="2001" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="2001" />
      <DstRect xOff="0" yOff="1500" xSize="2001" ySize="2001" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile6/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 48, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 48, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 48, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 48, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="2001" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="2001" />
      <DstRect xOff="2000" yOff="1500" xSize="2001" ySize="2001" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile7/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 56, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 56, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 56, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 56, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="1001" RasterYSize="2001" DataType="Float32" BlockXSize="1001" BlockYSize="2" />
      <SrcRect xOff="0" yOff="0" xSize="1001" ySize="2001" />
      <DstRect xOff="4000" yOff="1500" xSize="1001" ySize="2001" />
      <NODATA>-999</NODATA>
    </ComplexSource>
    <ComplexSource>
      <SourceFilename relativeToVRT="0">/vsicurl/http://ldm.cybercommons.org/tile8/''')
        _v = VFFSL(SL,"FOLDER",True) # u'$FOLDER' on line 64, col 84
        if _v is not None: write(_filter(_v, rawExpr=u'$FOLDER')) # from line 64, col 84.
        write(u'''/''')
        _v = VFFSL(SL,"FNAME",True) # u'$FNAME' on line 64, col 92
        if _v is not None: write(_filter(_v, rawExpr=u'$FNAME')) # from line 64, col 92.
        write(u'''</SourceFilename>
      <SourceBand>1</SourceBand>
      <SourceProperties RasterXSize="2001" RasterYSize="2001" DataType="Float32" BlockXSize="2001" BlockYSize="1" />
      <SrcRect xOff="0" yOff="0" xSize="2001" ySize="2001" />
      <DstRect xOff="5000" yOff="1500" xSize="2001" ySize="2001" />
      <NODATA>-999</NODATA>
    </ComplexSource>
  </VRTRasterBand>
</VRTDataset>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_UNQC_CREF= 'respond'

## END CLASS DEFINITION

if not hasattr(UNQC_CREF, '_initCheetahAttributes'):
    templateAPIClass = getattr(UNQC_CREF, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(UNQC_CREF)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=UNQC_CREF()).run()


