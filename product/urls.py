from django.conf import settings
from django.conf.urls import url

from product import views
from product.views import BrandAccountCreateView

app_name = "product"
urlpatterns = [
    url(r'^$', views.index, name="index"),

    url(r'^brand/add/$', views.brand_create, name="brand-add"),
    url(r'^brand/detail/$', views.brand_detail, name="brand-detail"),
    url(r'^brand/detail/(?P<bid>%s\d{7,13})/$' % settings.SLOG_PREFIX, views.brand_detail, name="brand-detail"),

    url(r'^brand-account/add/$', BrandAccountCreateView.as_view(), name="account-brand-add"),
]

