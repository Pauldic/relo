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

    club = context.filter(sTypes__sType='Club').count()
    convenience = context.filter(sTypes__sType='Convenience').count()
    dollar = context.filter(sTypes__sType='Dollar').count()
    liquor = context.filter(sTypes__sType='Liquor').count()
    grocery = context.filter(sTypes__sType='Grocery').count()
    mass = context.filter(sTypes__sType='Mass').count()
    military = context.filter(sTypes__sType='Military').count()
    pet = context.filter(sTypes__sType='Pet').count()

    data = {'context': context, 'accounts': accounts, 'stores': stores, 'club': club, 'convenience': convenience, 'dollar': dollar,
            'liquor': liquor, 'grocery': grocery, 'mass': mass, 'military': military, 'null_logo': null_logo, 'pet': pet}
    if is_api:
        data['context'] = 0

    return data
