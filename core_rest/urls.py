from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from core_rest import viewsets
from core_rest.view import ContextView

router_v1 = routers.DefaultRouter()
# router.register(r'core/api/v1/types', viewsets.TypeViewSet, base_name='type')
# router.register(r'core/api/v1/retailers', viewsets.RetailerAccountViewSet, base_name='retailer')
# router.register(r'core/api/v1/stores', viewsets.StoreAccountViewSet, base_name='store')

router_v1.register(r'types', viewsets.TypeViewSet, base_name='type')
router_v1.register(r'logos', viewsets.LogoUploadViewSet, base_name='logo')
router_v1.register(r'retailers', viewsets.RetailerAccountViewSet, base_name='retailer')
router_v1.register(r'stores', viewsets.StoreAccountViewSet, base_name='store')


schema_view = get_schema_view(title='Pastebin API')


app_name = "core-api"
urlpatterns = [
    url(r'^', include(router_v1.urls)),
    url(r'^context/$', ContextView.as_view(), name="context"),

]
