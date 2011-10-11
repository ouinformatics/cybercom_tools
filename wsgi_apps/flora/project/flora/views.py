from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from pymongo.connection import Connection
from pymongo import ASCENDING

import json
from pymongo import json_util


db = Connection().flora

def index(request):#,label=11):
    sel= db.endnote.find({"DataKeys":{"$exists" :True}},{'ShortTitle':1,'Label':1}).sort('Label',ASCENDING)
    data = {'select':sel}
    return render_to_response('index.html',data, context_instance = RequestContext( request ) )
def index_flora(request,label=11):
    #sel= db.endnote.find({"DataKeys":{"$exists" :True}},{'ShortTitle':1,'Label':1}).sort('Label',ASCENDING)
    data = {'label':label}
    return render_to_response('index_flora.html',data, context_instance = RequestContext( request ) )

def data(request,label=11):
    end = db.endnote.find({"Label":label})
    data = db.data.find({"_id":{"$in": end[0]['DataKeys']}})
    strdoc=''
    for doc in end:
        #strdoc=strdoc + _doc_to_json(doc)
        return HttpResponse(_doc_to_json(doc))

def _doc_to_json(doc):
        return json.dumps(doc,ensure_ascii=True,indent=4,default=json_util.default)
def index1( request ):    
    template = 'flora/index2.html'
    sel= db.endnote.find({"DataKeys":{"$exists" :True}},{'ShortTitle':1,'Label':1}).sort('Label',ASCENDING)
    #sel = db.data.find({},{'Sitename':1,'REF_NO':1}).sort('Label',ASCENDING)
    data = {'select':sel}
    return render_to_response( template, data, context_instance = RequestContext( request ) )

def ajax_bib_search( request ):
    q = request.GET.get( 'q' )
    dat='No Data'
    dat1='No Data'
    #avail = "T"
    ctab = 1
    if q is not None:
        try:
            q=int(q)
        except:
            q=-1
            #avail = "F"
        results = db.endnote.find({"Label":q,"DataKeys":{"$exists" :True}})
        if results.count() >0:
            dat = db.data.find({"_id":{"$in": results[0]['DataKeys']}})
            dat1 = db.data.find({"_id":{"$in": results[0]['DataKeys']}})
            dat2 = db.data.find({"_id":{"$in": results[0]['DataKeys']}})
        template = 'results.html'
        data = {'results': results,'dat' : dat,'dat1':dat1,'dat2':dat2,}
        #print data
        return render_to_response( template, data,context_instance = RequestContext( request ) )
    
