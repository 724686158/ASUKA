from django.conf.urls import url, include
from alchimest import views
from rest_framework import routers
from django.http import HttpResponse


router = routers.DefaultRouter()
router.register(r'package', views.PackageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^_ping/?$', lambda request: HttpResponse('working properly')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^package_list/$', views.package_list),
    url(r'^package_detail/(?P<namespace>[a-zA-Z0-9]*)/(?P<name>[a-zA-Z0-9]*)/(?P<tag>[a-zA-Z0-9]*)/$'.format(),
        views.package_detail),
]
