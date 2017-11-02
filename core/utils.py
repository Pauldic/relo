from django.conf import settings
from django.db.models import Q

from core.models import StoreAccount, RetailerAccount, Type


def get_real_id(slug):
    try:
        return int(slug[2:]) - settings.SLOG_VALUE
    except TypeError:
        return None


def context_data(is_api=False):
    context = RetailerAccount.objects.all()
    accounts = context.count()
    stores = StoreAccount.objects.all().count()
    null_logo = context.filter(Q(sLogo=None) | Q(sLogo="")).count()

    data = {'context': context, 'accounts': accounts, 'stores': stores, 'null_logo': null_logo, }

    types = Type.objects.all()

    for t in types:
        data[t.sType]=context.filter(sTypes__sType=t.sType).count()

    if is_api:
        data['context'] = 0

    return data
