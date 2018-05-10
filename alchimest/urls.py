from django.conf.urls import url, include
from alchimest import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'package', views.PackageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^release_list/$', views.package_list),
    url(r'^release_detail/(?P<namespace>[a-zA-Z0-9]*)/(?P<name>[a-zA-Z0-9]*)/(?P<tag>[a-zA-Z0-9]*)/$'.format(),
        views.release_detail),
]
