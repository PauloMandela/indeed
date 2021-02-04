from django.shortcuts import render
from django.views.generic.base import View
from .models import Country
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class MainPageView(View):
    def get(self, request):
        return render(request, 'index.html')
    
def getCountries(request):
    countries = []
    for c in Country.objects.all():
        countries.append(c.serializeCustom())
    # JsonResponse(countries)
    countries = {"countries":countries}
    return JsonResponse(countries, safe=False)

def banCountries(request):
    # return HttpResponse("ok", 200)
    cid = request.GET.get('id')
    ban = request.GET.get('ban')
    try:
        country = Country.objects.get(id=cid)
        if ban == "true":
            country.banned = True
        else:
            country.banned = False
        country.save()
        return JsonResponse(country.serializeCustom(), safe=False)
    except ObjectDoesNotExist:
        return HttpResponse("nocounty", 200)

def banAllCountries(request):
    if request.GET.get('ban') == "true":
        banned = True
    else:
        banned = False
    for c in Country.objects.all():
        c.banned = banned
        c.save()
    return HttpResponse("ok", 200)

    
    
