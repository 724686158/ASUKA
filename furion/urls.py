from django.conf.urls import url, include
from furion import views
from rest_framework import routers
from django.http import HttpResponse

router = routers.DefaultRouter()
router.register(r'environment', views.EnvironmentViewSet)
router.register(r'partner_variable', views.PartnerVariableViewSet)
router.register(r'partner_variable_in_environment', views.PartnerVariableInEnvironmentViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^_ping/?$', lambda request: HttpResponse('working properly')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^environment_list/$', views.environment_list),
    url(r'^environment_detail/(?P<environment>[a-zA-Z0-9_]*)/$'.format(),
        views.environment_detail),
]
