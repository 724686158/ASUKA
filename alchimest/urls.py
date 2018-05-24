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
    url(r'^package_detail/(?P<namespace>[a-zA-Z0-9_]*)/(?P<name>[a-zA-Z0-9_]*)/(?P<tag>[a-zA-Z0-9_]*)/$'.format(),
        views.package_detail),
    url(r'^glm_tree/(?P<type>[a-zA-Z0-9_]*)/(?P<name>[a-zA-Z0-9_]*)/$', views.glm_tree),
    url(r'^get_glm_tree_data/(?P<type>[a-zA-Z0-9_]*)/(?P<name>[a-zA-Z0-9_]*)/$', views.glm_tree_data, name='get_tree_data'),
    url(r'^dump_data/(?P<id>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/$', views.dump_data),
    url(r'^load_data/(?P<id>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/$', views.load_data),
]
