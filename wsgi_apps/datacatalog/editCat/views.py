# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import models
from cybercom.data.catalog import datalayer
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
import datetime
from django.contrib.auth.models import User
#from xmlrpclib import ServerProxy
#from rpc4django.utils import CookieTransport
#rpcURL = 'http://127.0.0.1:8000/RPC2/'
try:
    import json
except ImportError:
    import simplejson
def new_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST['name'], request.POST['email'] , request.POST['password'])
            md= datalayer.Metadata()
            md.Inserts('dt_people',[{"people_id":request.POST['name'],"person_name":request.POST['name'],"email":request.POST['email']}])
            #load example to everyones commons
            try:
                md.Inserts('dt_contributors',[{"commons_id" :803 ,"people_id" :request.POST['name']}])
            except:
                pass
            return HttpResponse("New User " + request.POST['name'] + " created successfully.")
        except Exception as inst:
            return HttpResponse(str(inst))
    else:
        return HttpResponse("[]")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/dataportal/accounts/login/?next=/dataportal/')
def webservice_view(request):
    try:
        methid = request.GET.get( 'method' )
        head = methid 
        if methid == 'catalog.dtCatalog':
            return render_to_response('editCat/ws2_results.html',{'header':head,'method':methid})
        if methid == 'catalog.dataCommons':
            return render_to_response('editCat/ws_results.html',{'header':head,'method':methid})
        if methid == 'catalog.EventResult':
            return render_to_response('editCat/ws3_results.html',{'header':head,'method':methid})
    except Exception as inst:
        return HttpResponse(str(inst))
#************** Formset Commons ******************************
#@login_required(login_url='accounts/login/')
@login_required()
def main_catalog(request):
    '''Table form style call'''
    userid=str(request.user)
    #md= datalayer.Metadata()
    DatacommonsFormSet = modelformset_factory(models.DtCatalog)
    if request.method == 'POST':
        formset = DatacommonsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = DatacommonsFormSet()
    return render_to_response('editCat/dtcommons.html', {'formset': formset})
# ************* Empty load ******************************************************************
@login_required()
def empty_Load(request):
    '''Load text '''
    return HttpResponse("<h1>Please select record or add new record!<h1>") 
#*******************************************************************************************
@login_required()
def ajax_result_del(request):
    commonid = request.GET.get( 'common_id' )
    eventid = request.GET.get( 'event_id' )
    try:
        c_id=int(commonid)
        c_id=int(eventid)
        checkAccess(str(request.user),commonid)
        c_id=int(commonid)
        md= datalayer.Metadata()
        md.Delete('dt_result',where="event_id = " + eventid)
        md.Delete('dt_event',where="event_id = " + eventid)
        #d = models.DtDataCommons.objects.get(commons_id=commonid)
        #print d
        #d.delete()
        return HttpResponse("true")
    except Exception as inst:
        return HttpResponse(str(inst))

@login_required()
def ajax_result(request):
    try:
        if request.method == 'POST':
            #varid=request.POST['var_id']
            #print request.POST
            #result_id= 
            #varid = request.META['QUERY_STRING'].split('=')[1]
            if varid != 'addnew':
                #x = int(eventid)
                rst = models.DtResult.objects.get(event_id = request.POST['event_id'], result_id = request.POST['result_id')#var = varid)
                form = models.DtResultForm(request.POST,request.FILES,instance = rst)
            else:
                form = models.DtResultForm(request.POST,request.FILES)
            checkAccess(str(request.user),request.POST['commons_id'])
            response = {'Success':'true'}
            #form.save()
            if form.is_valid():
                form.cleaned_data#().save()
                form.save()
                return HttpResponse(str(response))
            else:
                response.update( {'Success':'false'})
                err = {}
                for e in form.errors.iteritems():
                    err.update({e[0]:unicode(e[1])})
                response.update({'errors':err})
                return HttpResponse(str(response))
        else:
            resultid = request.GET.get('result_id')
            #varid = request.GET.get( 'var_id' )
            eventid = request.GET.get( 'event_id' )
            if resultid != 'addnew':
                x=int(eventid)
                result = models.DtResult.objects.get(event_id=eventid,result_id=resultid)#var=varid)

                #catid = event.cat_id
                #print "after com"
                form = models.DtResultForm(instance=result)
                #print "after form"
                #md= datalayer.Metadata()
                #sqlWhere = "event_id = " + eventid
                #data= md.Search('dt_result',where=sqlWhere,column=['var_id','result_text'])
            else:
                eventid = request.GET.get( 'event_id' )
                commm = request.GET.get( 'commons_id' )
                #print eventid
                form = models.DtResultForm(initial={"commons_id":commm,"event_id":eventid,"status_flag":"A","userid":str(request.user),"timestamp_created":datetime.datetime.now() })
                #data=[]
        action='getresult/?result_id=' + resultid
        c={'form':form,'action':action,'eventid':eventid,'resultid':resultid}#varid}
        c.update(csrf(request))
        return render_to_response('editCat/result.html',c)#dtcatalog.html',c)# {
    except Exception as inst:
        return HttpResponse(str(inst))



#*************** Event **********************************************************************
@login_required()
def load_event(request):
    try:

        commonid = request.GET.get( 'commons_id' )
        catid = request.GET.get( 'cat_id' )
        x = int(commonid)
        x = int(catid)
        userid=str(request.user)
        md= datalayer.Metadata()
        commons=''
        sqlWhere = "commons_id = " + commonid + " AND cat_id = " + catid + " ORDER BY event_id"
        data= md.Search('dt_event',where=sqlWhere,column=['event_id','event_name'],isPage=True,page=1,result_per_page=1000)
        c={'data':data,'commons':commons}
        return render_to_response('editCat/select_event.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
@login_required()
def ajax_event_del(request):
    commonid = request.GET.get( 'common_id' )
    eventid = request.GET.get( 'event_id' )
    try:
        c_id=int(commonid)
        c_id=int(eventid)
        checkAccess(str(request.user),commonid)
        c_id=int(commonid)
        md= datalayer.Metadata()
        md.Delete('dt_result',where="event_id = " + eventid)
        md.Delete('dt_event',where="event_id = " + eventid)
        #d = models.DtDataCommons.objects.get(commons_id=commonid)
        #print d
        #d.delete()
        return HttpResponse("true")
    except Exception as inst:
        return HttpResponse(str(inst))

@login_required()
def ajax_event(request):
    try:
        if request.method == 'POST':
            eventid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if eventid != 'addnew':
                x = int(eventid)
                evt = models.DtEvent.objects.get(event_id=eventid)
                form = models.DtEventForm(request.POST,request.FILES,instance=evt)
            else:
                form = models.DtEventForm(request.POST,request.FILES)
            checkAccess(str(request.user),request.POST['commons_id'])
            response = {'Success':'true'}
            if form.is_valid():
                form.cleaned_data#().save()
                form.save()
                return HttpResponse(str(response))
            else:
                response.update( {'Success':'false'})
                err = {}
                for e in form.errors.iteritems():
                    err.update({e[0]:unicode(e[1])})
                response.update({'errors':err})
                return HttpResponse(str(response))
        else:
            eventid = request.GET.get( 'event_id' )
            if eventid != 'addnew':
                x=int(eventid)
                event = models.DtEvent.objects.get(event_id=eventid)
                catid = event.cat_id
                #print "after com"
                form = models.DtEventForm(instance=event)
                #print "after form"
                md= datalayer.Metadata()
                sqlWhere = "event_id = " + eventid
                data= md.Search('dt_result',where=sqlWhere,column=['var_id','result_text','result_id'])
            else:
                catid = request.GET.get( 'catid' )
                commm = request.GET.get( 'commons_id' )
                form = models.DtEventForm(initial={"commons_id":commm,"cat_id":catid,"status_flag":"A","userid":str(request.user),"timestamp_created":datetime.datetime.now() })
                data=[]
        action='getevent/?event_id=' + str(eventid)
        c={'form':form,'action':action,'data':data,'eventid':eventid,'catid':catid}
        c.update(csrf(request))
        return render_to_response('editCat/event_result.html',c)#dtcatalog.html',c)# {
    except Exception as inst:
        return HttpResponse(str(inst))

#**************  Commons  **********************************************************************
#@login_required(login_url='accounts/login/')
@login_required()
def main_commons(request):
    userid=str(request.user)
    md= datalayer.Metadata()
    commons=''
    sqlWhere = "commons_id in (select commons_id from dt_contributors where people_id ='" + userid + "')" + " ORDER BY commons_id"
    data= md.Search('dt_data_commons',where=sqlWhere,column=['commons_id','commons_code'])
    c={'data':data,'commons':commons}
    return render_to_response('editCat/commons.html',c)

@login_required()
def load_common(request):
    userid=str(request.user)
    md= datalayer.Metadata()
    commons=''
    sqlWhere = "commons_id in (select commons_id from dt_contributors where people_id ='" + userid + "')" + " ORDER BY commons_id"
    data= md.Search('dt_data_commons',where=sqlWhere,column=['commons_id','commons_code'])
    c={'data':data,'commons':commons,'user':str(request.user)}
    return render_to_response('editCat/select_commons.html',c)

@login_required()
def ajax_com_del(request):
    commonid = request.GET.get( 'common_id' )
    try:
        checkAccess(str(request.user),commonid)
        c_id=int(commonid)
        md= datalayer.Metadata()
        md.Delete('dt_result',where="commons_id = " + commonid)
        md.Delete('dt_event',where="commons_id = " + commonid)
        md.Delete('dt_catalog',where="commons_id = " + commonid)
        md.Delete('dt_contributors',where="commons_id = " + commonid)
        md.Delete('dt_data_commons',where="commons_id = " + commonid)
        return HttpResponse("true")
    except Exception as inst:
        return HttpResponse(str(inst))
@login_required()
def ajax_com(request):
    commonid=''
    if request.method == 'POST':
        commonid = request.META['QUERY_STRING'].split('=')[1]
        #print request
        if commonid != 'addnew':
            com = models.DtDataCommons.objects.get(commons_id=commonid)
            form = models.DtDataCommonsForm(request.POST,request.FILES,instance=com)
        else:
            form = models.DtDataCommonsForm(request.POST,request.FILES)
        
        response= {'Success':'true'}
        if form.is_valid():
            form.cleaned_data
            savedform=form.save()
            if commonid == 'addnew':
                checkuserid(str(request.user))
                md= datalayer.Metadata()
                c_id = savedform.commons_id
                md.Inserts('dt_contributors',[{"commons_id" : c_id ,"people_id" : str(request.user)}])
            #json = simplejson.dumps(response, ensure_ascii=False)
            return HttpResponse(str(response))#json, mimetype='application/javascript')
        else:
            response.update({'Success':'false'})
            err={}
            for e in form.errors.iteritems():
                err.update({e[0]:unicode(e[1])}) 
            response.update({'errors':err})
            #response = json_response({ 'success' : False,'errors' : [(k, v[0].__unicode__()) for k, v in form.errors.items()] })
            #print response
            #response = form.errors_as_json()
            #json = simplejson.dumps(response, ensure_ascii=False)
            return HttpResponse(str(response))#json, mimetype='application/javascript')#json.dumps(response, ensure_ascii=False),mimetype='application/json')
            #return render_to_response("Saved Record")#HttpResponseRedirect('/thanks/')
    else:
        commonid = request.GET.get( 'common_id' )
       # deletes=''
       # try:
       #     deletes = request.GET.get( 'delete' )
       #     err=models.DtDataCommons.objects.get(commons_id=commonid).delete()
       # except:
       #     pass
        if commonid != 'addnew':
            com = models.DtDataCommons.objects.get(commons_id=commonid)
            form = models.DtDataCommonsForm(instance=com)
        else:
            form = models.DtDataCommonsForm(initial={"status_flag":"A","start_date":datetime.datetime.now() })
    action="getcommon/?common_id=" + str(commonid) 
    c={'form':form,'action':action,'commonid':commonid,'user':str(request.user)}
    c.update(csrf(request))
    return render_to_response('editCat/com_result.html',c)#dtcatalog.html',c)# {
#************************** Catalog ***************************************************************


@login_required()
def catalog(request,commons=None):
    '''Setup for catalog ajax_cat function'''
    userid=str(request.user)
    md= datalayer.Metadata()
    commonid = request.GET.get( 'common_id' )
    commons ='commons_id=' + commonid + " ORDER BY observed_date desc , loc_id " # md.Search('dt_data_commons',where=where,column=['commons_id','commons_name'])

    #****************************hookup later************************
    data= md.Search('dt_catalog',where=commons,column=['cat_id','cat_name'],isPage=True,page=1,result_per_page=1000)
    #print data
    c={'data':data,'commons':commons,'user':str(request.user)}
    return render_to_response('editCat/select_catalog.html',c)#dtcatalog.html',c)# {

@login_required()
def ajax_cat_del(request):
    #commonid = request.GET.get( 'common_id' )
    #catid = request.GET.get( 'cat_id' )
    try:
        commonid = request.GET.get( 'common_id' )
        catid = request.GET.get( 'cat_id' )
        c_id=int(commonid)
        c_id=int(catid)
        checkAccess(str(request.user),commonid)
        #c_id=int(commonid)
        md= datalayer.Metadata()
        md.Delete('dt_result',where="event_id in(select event_id from dt_event where cat_id= " + catid + ")")
        md.Delete('dt_event',where="cat_id = " + catid)
        md.Delete('dt_catalog',where="cat_id = " + catid)
        #md.Delete('dt_data_commons',where="commons_id = " + commonid)
        #d = models.DtDataCommons.objects.get(commons_id=commonid)
        #print d
        #d.delete()
        return HttpResponse("true")
    except Exception as inst:
        return HttpResponse(str(inst))

@login_required()
def ajax_cat(request):
    if request.method == 'POST':
        catid = request.META['QUERY_STRING'].split('=')[1]#[tid
        if catid != 'addnew':
            cat = models.DtCatalog.objects.get(cat_id=catid)
            form = models.DtCatalogForm_data(request.POST,request.FILES,instance=cat)
        else:
            form = models.DtCatalogForm_data(request.POST,request.FILES)
        response = {'Success':'true'}
        try:
            if form.is_valid():
                form.cleaned_data#().save()
                form.save()
                return HttpResponse("{'result':'Success'}")
            else:
                response.update({'Success':'false'})
                err={}
                for e in form.errors.iteritems():
                    err.update({e[0]:unicode(e[1])})
                response.update({'errors':err})
                return HttpResponse(str(response))#json.dumps(response, ensure_ascii=False),mimetype='application/json')
        except Exception as inst:
            return HttpResponse(str(inst))
    else:
        try:
            catid = request.GET.get( 'catid' ) 
            if catid != 'addnew':
                cat = models.DtCatalog.objects.get(cat_id=catid)
                form = models.DtCatalogForm_data(instance=cat)
                commm = cat.commons_id
                print commm
            else:
                commm = request.GET.get( 'commons_id' )
                form = models.DtCatalogForm_data(initial = {"commons_id": commm,"status_flag":"A","userid":str(request.user),"timestamp_created":datetime.datetime.now() })
            form.fields['loc_id'].queryset = models.DtLocation.objects.filter(commons_id= commm)
            action='getcatalog/?catid=' + str(catid)
            c={'form':form,'action':action,'catid':catid,'user':str(request.user),'commonsid':commm}
            c.update(csrf(request))
            return render_to_response('editCat/cat_result.html',c)#dtcatalog.html',c)# {
        except Exception as inst:
            return HttpResponse(str(inst))
#*************************Location **********************************************************************
@login_required()
def ajax_loc(request):
    try:
        if request.method == 'POST':
            locid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if locid != 'addnew':
                loc = models.DtLocation.objects.get(loc_id=locid,commons_id=request.POST['commons_id'])
                form = models.DtLocationForm(request.POST,request.FILES,instance=loc)
            else:
                form = models.DtLocationForm(request.POST,request.FILES)
            response = {'Success':'true'}
            try:
                if form.is_valid():
                    form.cleaned_data
                    form.save()
                    return HttpResponse( str(response))#"{'result':'Success'}")
                else:
                    response.update({'Success':'false'})
                    err={}
                    for e in form.errors.iteritems():
                        err.update({e[0]:unicode(e[1])})
                    response.update({'errors':err})
                    return HttpResponse(str(response))
            except Exception as inst:
                return HttpResponse(str(inst))
        else:
            comid = request.GET.get( 'commons_id' )
            locid = request.GET.get( 'loc_id' )

            if locid != 'addnew':
                loc = models.DtLocation.objects.get(loc_id=locid,commons_id=comid)
                form = models.DtLocationForm(instance=loc)
            else:
                commm = request.GET.get( 'commons_id' )
                form = models.DtLocationForm(initial = {"commons_id": commm})
        action='getlocation/?locid=' + str(locid)
        c={'form':form,'action':action,'header':'Location'}
        c.update(csrf(request))
        return render_to_response('editCat/loc_result.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
#************************* Method **********************************************************************
@login_required()
def ajax_meth(request):
    try:
        if request.method == 'POST':
            methid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if methid != 'addnew':
                meth = models.RtMethod.objects.get(method_code=methid)
                form = models.RtMethodForm(request.POST,request.FILES,instance=meth)
            else:
                form = models.RtMethodForm(request.POST,request.FILES)
            response = {'Success':'true'}
            try:
                if form.is_valid():
                    form.cleaned_data
                    form.save()
                    return HttpResponse( str(response))#"{'result':'Success'}")
                else:
                    response.update({'Success':'false'})
                    err={}
                    for e in form.errors.iteritems():
                        err.update({e[0]:unicode(e[1])})
                    response.update({'errors':err})
                    return HttpResponse(str(response))
            except Exception as inst:
                return HttpResponse(str(inst))
        else:
            comid = request.GET.get( 'commons_id' )
            methid = request.GET.get( 'method_id' )

            if methid != 'addnew':
                meth = models.RtMethod.objects.get(method_code=methid)
                form = models.RtMethodForm(instance=meth)
                md= datalayer.Metadata()
                sqlWhere = "method_code = '" + methid + "'"
                data= md.Search('rt_method_parameters',where=sqlWhere,column=['param_name','param_desc','param_value','method_id'])
            else:
                commm = request.GET.get( 'commons_id' )
                form = models.RtMethodForm(initial = {"commons_id": commm,'status_flag':'A',"userid":str(request.user)})
                data=[]
        action='getmethod/?method_id=' + str(methid)
        c={'form':form,'action':action,'data':data,'header':'Method'}
        c.update(csrf(request))
        return render_to_response('editCat/meth_result.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
#************************* Meth Par  **********************************************************************
@login_required()
def ajax_methPar(request):
    try:
        if request.method == 'POST':
            if str(request.user) != request.POST['userid']:
                return HttpResponse( str(request.user) + " is not authorized to update record.\n" +
                            " Record must be updated by record creator.")
            typeid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if typeid != 'addnew':
                print typeid
                typ = models.DtType.objects.get(type_id=typeid)
                form = models.DtTypeForm(request.POST,request.FILES,instance=typ)
            else:
                print "new"
                form = models.DtTypeForm(request.POST,request.FILES)
            response = {'Success':'true'}
            try:
                print request.POST
                if form.is_valid():
                    form.cleaned_data
                    form.save()
                    return HttpResponse( str(response))#"{'result':'Success'}")
                else:
                    response.update({'Success':'false'})
                    err={}
                    for e in form.errors.iteritems():
                        err.update({e[0]:unicode(e[1])})
                    response.update({'errors':err})
                    return HttpResponse(str(response))
            except Exception as inst:
                return HttpResponse(str(inst))
        else:
            #comid = request.GET.get( 'commons_id' )
            methid = request.GET.get( 'method_code' )

            if methid != 'addnew':
                tpe = models.RtMethodParameters.objects.get(method_id=methid)
                form = models.RtMethodParametersForm(instance=tpe)
            else:
                #commm = request.GET.get( 'commons_id' )
                form = models.RtMethodParametersForm()#initial = {"commons_id": commm,"userid":str(request.user)})
        action='getmethPar/?method_code=' + str(methid)
        c={'form':form,'action':action,'header':'Method Parameter','methcode':str(methid)}
        c.update(csrf(request))
        return render_to_response('editCat/loc_result.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
#************************* Type  **********************************************************************
@login_required()
def ajax_type(request):
    try:
        if request.method == 'POST':
            if str(request.user) != request.POST['userid']:
                return HttpResponse( str(request.user) + " is not authorized to update record.\n" +
                            " Record must be updated by record creator.")
            typeid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if typeid != 'addnew':
                print typeid
                typ = models.DtType.objects.get(type_id=typeid)
                form = models.DtTypeForm(request.POST,request.FILES,instance=typ)
            else:
                print "new"
                form = models.DtTypeForm(request.POST,request.FILES)
            response = {'Success':'true'}
            try:
                print request.POST
                if form.is_valid():
                    form.cleaned_data
                    form.save()
                    return HttpResponse( str(response))#"{'result':'Success'}")
                else:
                    response.update({'Success':'false'})
                    err={}
                    for e in form.errors.iteritems():
                        err.update({e[0]:unicode(e[1])})
                    response.update({'errors':err})
                    return HttpResponse(str(response))
            except Exception as inst:
                return HttpResponse(str(inst))
        else:
            comid = request.GET.get( 'commons_id' )
            typeid = request.GET.get( 'type_id' )

            if typeid != 'addnew':
                tpe = models.DtType.objects.get(type_id=typeid)
                form = models.DtTypeForm(instance=tpe)
            else:
                commm = request.GET.get( 'commons_id' )
                form = models.DtTypeForm(initial = {"commons_id": commm,"userid":str(request.user)})
        action='gettype/?type_id=' + str(typeid)
        c={'form':form,'action':action,'header':'Data Type'}
        c.update(csrf(request))
        return render_to_response('editCat/loc_result.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
#************************* Variables  **********************************************************************
@login_required()
def ajax_var(request):
    try:
        if request.method == 'POST':
            if str(request.user) != request.POST['userid']:
                return HttpResponse( str(request.user) + " is not authorized to update record.\n" +
                            " Record must be updated by record creator.")
            varid = request.META['QUERY_STRING'].split('=')[1]#[tid
            if varid != 'addnew':
                typ = models.RtVariables.objects.get(var_id=varid)
                form = models.RtVariablesForm(request.POST,request.FILES,instance=typ)
            else:
                form = models.RtVariablesForm(request.POST,request.FILES)
            response = {'Success':'true'}
            try:
                if form.is_valid():
                    form.cleaned_data
                    form.save()
                    return HttpResponse( str(response))#"{'result':'Success'}")
                else:
                    response.update({'Success':'false'})
                    err={}
                    for e in form.errors.iteritems():
                        err.update({e[0]:unicode(e[1])})
                    response.update({'errors':err})
                    return HttpResponse(str(response))
            except Exception as inst:
                return HttpResponse(str(inst))
        else:
            varid = request.GET.get( 'var_id' )
#RtVariablesForm
            if varid != 'addnew':
                tpe = models.RtVariables.objects.get(var_id=varid)
                form = models.RtVariablesForm(instance=tpe)
            else:
                form = models.RtVariablesForm(initial = {"userid":str(request.user),'status_flag':'A'})
        action='getvar/?var_id=' + str(varid)
        c={'form':form,'action':action,'header':'Variables'}
        c.update(csrf(request))
        return render_to_response('editCat/loc_result.html',c)
    except Exception as inst:
        return HttpResponse(str(inst))
#***************************** Security *******************************************************
def checkAccess(username,id,type='commons'):
    md=datalayer.Metadata()
    if type == 'commons':
        r=md.Search('dt_contributors',where="people_id = '" + str(username)  + "' and commons_id=" + str(id))
        if r==[]:
            raise Exception("Permission Error","User: " + username + " does not have write access to Data Commons( id = " + str(id) + ")")
    elif type == 'catalog':
        pass
def checkuserid(username):
    md=datalayer.Metadata()
    r=md.Search('dt_people',where="people_id = '" + str(username) + "'")
    if r==[]:
        #md.Inserts('dt_contributors',[{"commons_id" : c_id ,"people_id" : str(request.user)}])
        md.Inserts('dt_people',[{"people_id" : str(username)}])
         


