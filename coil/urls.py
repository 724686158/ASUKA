from django.conf.urls import url
from coil import views
from django.http import HttpResponse
from django.http import JsonResponse


urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^_ping/?$', lambda request: HttpResponse("working properly")),
    url(r'^dump_data/', lambda request: JsonResponse(data=views.dump_data())),
    url(r'^load_data/', lambda request: JsonResponse(data=views.load_data())),
    url(r'^link_test/(?P<environment_name>[a-zA-Z0-9_]*)/(?P<package_namespace>[a-zA-Z0-9_]*)/(?P<package_name>[a-zA-Z0-9_]*)/(?P<package_tag>[a-zA-Z0-9_]*)/$', views.LinkView.as_view()),
    # url(r'^link/', ),
]
