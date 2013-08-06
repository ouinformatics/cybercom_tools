# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout,authenticate,views
from django.contrib.auth.models import User
from cybercom.data.catalog import datalayer
import json
from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def new_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST['name'], request.POST['email'] , request.POST['password'])
            #load example to everyones commons
            try:
                md= datalayer.Metadata()
                md.Inserts('dt_people',[{"people_id":request.POST['name'],"person_name":request.POST['name'],"email":request.POST['email']}])
                md.Inserts('dt_contributors',[{"commons_id" :803 ,"people_id" :request.POST['name']}])
            except:
                pass
            return HttpResponse("New User " + request.POST['name'] + " created successfully.")
        except Exception as inst:
            return HttpResponse(str(inst))
    else:
        return HttpResponse("[]")
def login(request, template_name='registration/login.html'):
    clear =request.REQUEST.get('clear', '')
    response = views.login(request,template_name=template_name)
    if not clear =='':
        request.environ['authtkt.forget'](request, response)
    return response
def logout_view(request,redirect=None,template_name='registration/logout.html'):
    #django.contrib.auth.views.logout_then_login
    response = views.logout_then_login(request)
    request.environ['authtkt.forget'](request, response)
    return response
@login_required()
def profile(request):
    u = User.objects.get(username__exact= request.user )
    if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
        name = u.username
    else:
        name = u.get_full_name()
    try:
        md= datalayer.Metadata()
        host= request.get_host()
        baseurl = request.get_host()#'www.cybercommons.org' 
        where = "event_id in (select event_id from dt_event where commons_id=814 and event_name='%s') order by result_order" % (baseurl)
        data = md.Search('dt_result',where=where,column=['var_id','result_text','result_type','remark'])
    except:
        data=[]
    return render_to_response('registration/profile.html',{'user':name,'baseAccount_path':'/accounts/','apps':data,'host':host})
def cherrypy_userdata(request,**kwargs):
    callback = request.GET.get('callback', None)
    user_id = int(request.GET.get('user', '0'))
    try:
        u = User.objects.get(id=user_id )
        if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
            name = u.username
        else:
            name = u.get_full_name()
        prof ={'username':u.username,'name':name}
    except:
        prof={'username':'guest','name':'guest'}
    if callback:
        return HttpResponse('%s(%s)' % (callback,json.dumps({'user':prof},indent=2)))
    return HttpResponse( json.dumps({'user':prof},indent=2) )
    #return HttpResponse(str(request.environ['authtkt.identify']))

def userdata(request,**kwargs):
    callback = request.GET.get('callback', '')
    try:
        uid= request.user.id
    except:
        uid=0
    try:
        u = User.objects.get(username__exact= request.user )
        if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
            name = u.username
        else:
            name = u.get_full_name()
        prof ={'username':u.username,'name':name,'id':str(uid)}
    except:
        try:
            u = User.objects.get(id= int(request.user) )
            if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
                name = u.username
            else:
                name = u.get_full_name()
            prof ={'username':u.username,'name':name,'id':str(uid)}
        except:
            prof={'username':'guest','name':'guest','id':str(uid)}
    #return JsonResponse(prof,callback=callback)#request.GET.get('jsoncallback'))
    #if request.environ['REMOTE_USER']
    if callback != '':
        try:
            return  HttpResponse( str(callback) + "(" + json.dumps({'user':prof},indent=2) + ")" )
            request.environ['authtkt.identify'](request,response)
            return response
        except:
            prof={'username':'guest','name':'guest'}
            return HttpResponse( str(callback) + "(" + json.dumps({'user':prof},indent=2) + ")" )
    else:
        try:
            return HttpResponse( json.dumps({'user':prof},indent=2) )
            request.environ['authtkt.identify'](request,response)
            return response
        except:
            prof={'username':'guest','name':'guest'}
            return HttpResponse( json.dumps({'user':prof},indent=2) )
