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
__CHEETAH_genTime__ = 1331835374.355819
__CHEETAH_genTimestamp__ = 'Thu Mar 15 13:16:14 2012'
__CHEETAH_src__ = 'base_html.tmpl'
__CHEETAH_srcLastModified__ = 'Thu Mar 15 13:15:28 2012'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class base_html(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(base_html, self).__init__(*args, **KWs)
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
        
        write(u'''<!DOCTYPE html>
<html>
<head>
<title>Cybercommons Data</title>
<!--BaseJavascript-->
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery-1.7.2.min.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery.jeditable.mini.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery-ui-1.8.10.custom.min.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/mstacy/jquery.contextMenu.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/css/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/pagination/jquery.pagination.js"></script>
<!--Base CSS-->
<link type="text/css" href="http://static.cybercommons.org/css/cybercomui/jquery-ui-1.8.13.custom.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/css/bootstrap/css/bootstrap.min.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/css/bootstrap/css/cybercommons.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/css/cybercom/style.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/pagination/pagination.css" rel="Stylesheet"/>
<!--Custom App JS-CSS-->
<script type="text/javascript" src="http://static.cybercommons.org/ref/mongodb/filter.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/ref/mongodb/json.js"></script>
<link type="text/css" src="http://static.cybercommons.org/pagination/pagination.css" rel="stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/ref/mongodb/json.css" rel="Stylesheet"/>


<!--<link type="text/css" href="http://static.cybercommons.org/css/cybercomui/jquery-ui-1.8.13.custom.css" rel="Stylesheet"/>
<link type="text/css" rel="stylesheet" href="http://static.cybercommons.org/css/bootstrp/bootstrap.min.css"/>
<link type="text/css" href="http://static.cybercommons.org/css/cybercom/style.css" rel="Stylesheet"/>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery-1.7.min.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery-ui-1.8.10.custom.min.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery.form.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/js/jquery.jeditable.mini.js"></script>
<link type="text/css" href="http://static.cybercommons.org/css/cybercomui/jquery-ui-1.8.13.custom.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/css/cybercom/style.css" rel="Stylesheet"/>
<link type="text/css" href="http://static.cybercommons.org/ref/mongodb/json.css" rel="Stylesheet"/>
<link type="text/css" src="http://static.cybercommons.org/pagination/pagination.css" rel="stylesheet"/>
<script type="text/javascript" src="http://static.cybercommons.org/ref/mongodb/filter.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/ref/mongodb/json.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/mstacy/jquery.contextMenu.js"></script>
<script type="text/javascript" src="http://static.cybercommons.org/pagination/jquery.pagination.js"></script>-->
<style>
    #feedback { font-size: 1.4em; }
    #selectable .ui-selecting { background: #E7E1D3; }
    #selectable .ui-selected { background: #005C81; color: white; }
    #selectable { list-style-type: none; margin: 0; padding: 0; width: 90%; }
    #selectable li { margin: 1px; padding: 0.2em; }
</style>
<script>
qry ='{}'
$(document).ready(function() { 
    $('#rst_fields').hide();
    $('#rst_filter').hide();
    var options = { 
        target:        \'#output1\',   // target element(s) to be updated with server response 
        //beforeSubmit:  showRequest,  // pre-submit callback 
        //success:       showResponse  // post-submit callback 
 
        // other available options: 
        //url:       url         // override for form\'s \'action\' attribute 
        //type:      type        // \'get\' or \'post\', override for form\'s \'method\' attribute 
        //dataType:  null        // \'xml\', \'script\', or \'json\' (expected server response type) 
        //clearForm: true        // clear all form fields after successful submit 
        //resetForm: true        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        //timeout:   3000 
    }; 
    //Field Dialog
        $( \'#field-dialog\' ).dialog({
            autoOpen: false,
           // width:500,
            async:true,
            title:"Select Fields",
           // height:795,
            modal: true,
            buttons: {
                Ok: function() {
                    $(\'#field-dialog\').dialog(\'close\');
                }
            }
        });
    $( \'#query\' ).button();
    $( \'#export\' ).button();
    $( \'#fopener\' ).button();
    $( \'#fopener\' ).click(function() {
       $(\'#field-dialog\').dialog(\'open\');
    });
    $(\'#field-dialog\').bind(\'dialogclose\', function(event) {
       //Include All Fields
        var result = $( "#rst_fields" ).empty();
        $( ".ui-selected","#selectable").each(function() {
            result.append("\'" + $(this).text() + "\'," );
        });
    });
    //$(\'#accordion\' ).accordion(); 
    $( \'#selectable\' ).selectable();
    // bind form using \'ajaxForm\' 
    //$(\'.catform\').ajaxForm(options); 
    $(\'.edit\').editable(\'http://production.cybercommons.org/mongodb/save/\');
    var result = $( "#rst_fields" ).empty();
    $( ".ui-selected","#selectable").each(function() {
            result.append("\'" + $(this).text() + "\'," );
    });
});
</script>
</head>
</head>
<body>
''')
        _v = VFFSL(SL,"body",True) # u'@body' on line 44, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'@body')) # from line 44, col 1.
        write(u'''
</body>
</html>
''')
#<link type="text/css" rel="stylesheet" href="http://static.cybercommons.org/css/bootstrp/bootstrap.min.css"/>
#        
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

    _mainCheetahMethod_for_base_html= 'respond'

## END CLASS DEFINITION

if not hasattr(base_html, '_initCheetahAttributes'):
    templateAPIClass = getattr(base_html, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(base_html)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=base_html()).run()


