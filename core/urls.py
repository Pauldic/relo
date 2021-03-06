from django.conf import settings
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from core import views


app_name = "core"
urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^$', views.home, name="index"),
    url(r'^home/$', views.home),
    url(r'^index/$', views.home),
    url(r'^ping/$', views.ping),

    url(r'^add-type/$', views.type_add, name="add-type"),
    url(r'^edit-type/(?P<tid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.type_add, name="edit-type"),
    url(r'^type-detail/$', views.type_detail, name="type-detail"),
    url(r'^type-detail/(?P<rid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.type_detail, name="type-detail"),

    url(r'^add-retailer/$', views.retailer_add, name="add-retailer"),
    url(r'^edit-retailer/(?P<rid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.retailer_add, name="edit-retailer"),
    url(r'^retailer-detail/$', views.retailer_detail, name="retailer-detail"),
    url(r'^retailer-detail/(?P<rid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.retailer_detail, name="retailer-detail"),

    url(r'^add-store/$', views.store_add, name="add-store"),
    url(r'^edit-store/(?P<sid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.store_add, name="edit-store"),
    url(r'^store-detail/$', views.store_detail, name="store-detail"),
    url(r'^retailers-store/(?P<rid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.retailers_store, name="retailers-store"),


    url(r'^context/$', views.get_context, name="context"),

    # url(r'^api/%s/context/$' % settings.API_VERSION, views.ContextView.as_view(), name="api-context"),
    #
    # url(r'^api/%s/retailer/list/$' % settings.API_VERSION, views.api_retailer_list, name="api-retailer-list"),
    # url(r'^api/%s/retailer/list/(?P<pk>[0-9]+)/$' % settings.API_VERSION, views.api_retailer_detail, name="api-retailer-detail"),
    #
    # url(r'^api/%s/store/list/$' % settings.API_VERSION, views.api_store_list, name="api-store-list"),
    # url(r'^api/%s/store/list/(?P<pk>[0-9]+)/$' % settings.API_VERSION, views.api_store_detail, name="api-store-detail"),
    #
    # url(r'^api/%s/type/list/$' % settings.API_VERSION, views.api_type_list, name="api-type-list"),
    # url(r'^api/%s/type/list/(?P<pk>[0-9]+)/$' % settings.API_VERSION, views.api_type_detail, name="api-type-detail"),

]


# urlpatterns = format_suffix_patterns(urlpatterns)

