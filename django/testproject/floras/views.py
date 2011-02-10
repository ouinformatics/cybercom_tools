from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from testproject.floras.models import *
# Create your views here.
def search_form(request):
    return render_to_response('search_form.html')
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        DtCatalogs = DtCatalog.objects.filter(cat_name__regex=q)
        return render_to_response('search_results.html', {'cats':DtCatalogs,'query':q})
		#message = 'You searched for: %r' % request.GET['q']
    else:
        #message = 'You submitted an empty form.'
        return HttpResponse('Please submit a search term.')
