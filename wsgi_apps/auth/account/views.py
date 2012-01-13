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
def login(request, template_name='registration/login.html'):
    #django.contrib.auth.views.login
    response = views.login(request,template_name=template_name)
    if request.method == 'GET':
        logout(request)
    request.environ['authtkt.forget'](request, response)
    return response
def logout_view(request,redirect=None):
    logout(request)
    if redirect:
        url = '/accounts/login/?next= %s ' % (redirect)
    else:
        url = '/accounts/login/?next=/accounts/login/'
    return HttpResponseRedirect(url)#'accounts/login/?next=/dataportal/')
@login_required()
def profile(request):
    u = User.objects.get(username__exact= request.user )
    if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
        name = u.username
    else:
        name = u.get_full_name()
    html = "<h1> Welcome %s </h1><p> Thank you for visiting your profile page. Future development will allow you to set new passwords, share application data with other registered users, plus many other profile tasks.</p>" % (name) 
    return HttpResponse(html)
    return HttpResponse(str(dir(u)))#"[User account - Profile Page]")

def userdata(request,**kwargs):
    callback = request.GET.get('callback', '')
    try:
        u = User.objects.get(username__exact= request.user )
        if u.get_full_name() is None or u.get_full_name() == '' or u.get_full_name() == '>':
            name = u.username
        else:
            name = u.get_full_name()
        prof ={'username':u.username,'name':name}
    except:
        prof={'username':'guest','name':'guest'}
    #return JsonResponse(prof,callback=callback)#request.GET.get('jsoncallback'))
    if callback != '':
        return HttpResponse( str(callback) + "(" + json.dumps({'user':prof},indent=2) + ")" )
    else:
        return HttpResponse( json.dumps({'user':prof},indent=2) )
