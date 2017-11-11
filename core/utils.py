import boto3
from django.conf import settings
from django.db.models import Q
# from storages.backends.s3boto import S3BotoStorage

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
        data[t.sType] = context.filter(sTypes__sType=t.sType).count()

    if is_api:
        data['context'] = 0

    return data


# class CustomMediaS3BotoStorage(S3BotoStorage):
#     def __init__(self, *args, **kwargs):
#         super(CustomMediaS3BotoStorage, self).__init__(*args, **kwargs)
#
#     # def _save(self, *args, **kwargs):
#     #     return super(CustomS3BotoStorage, self)._save(*args, **kwargs)
#     def _save(self, name, content):
#         print(self.name)
#         print(self.content)
#         return super(CustomMediaS3BotoStorage, self)._save(name, content)


def copy_object(src_bucket_name,
                src_key_name,
                dst_bucket_name,
                dst_key_name,
                metadata=None,
                preserve_acl=True):
    """
    Copy an existing object to another location.

    src_bucket_name   Bucket containing the existing object.
    src_key_name      Name of the existing object.
    dst_bucket_name   Bucket to which the object is being copied.
    dst_key_name      The name of the new object.
    metadata          A dict containing new metadata that you want
                      to associate with this object.  If this is None
                      the metadata of the original object will be
                      copied to the new object.
    preserve_acl      If True, the ACL from the original object
                      will be copied to the new object.  If False
                      the new object will have the default ACL.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(src_bucket_name)

    # Lookup the existing object in S3
    key = bucket.lookup(src_key_name)

    # Copy the key back on to itself, with new metadata
    return key.copy(dst_bucket_name, dst_key_name, metadata=metadata, preserve_acl=preserve_acl)