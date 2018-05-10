from django.conf.urls import patterns
from django.conf.urls import url
from coil import views
from django.http import HttpResponse
from django.http import JsonResponse

urlpatterns = patterns(
    '',
    url(r'^_ping/?$', lambda request: HttpResponse("{}:{}".format("coil",
                                                                  "working"))),
    url(r'^_diagnose/?$', lambda request: JsonResponse(data=views.self_diagnose())),
    url(r'^dump_data/', lambda request: JsonResponse(data=views.dump_data())),
    url(r'^load_data/', lambda request: JsonResponse(data=views.load_data())),
    url(r'^link_test/', lambda request: JsonResponse(data=views.load_data())),
    url(r'^link/', lambda request: JsonResponse(data=views.load_data())),
)
