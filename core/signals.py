import os

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from shutil import copy2

from core.models import RetailerAccount


@receiver(post_save, sender=RetailerAccount, dispatch_uid="rename_uploaded_image")
def rename_image(sender, instance, created, **kwargs):
    try:
        if created:
            path = instance.sLogo.path
            path = path.replace(os.path.splitext(path)[0].split("/")[-1], str(instance.id)+os.path.splitext(path)[1])
            copy2(instance.sLogo.path, path)
            db_file = instance.sLogo.url.split(settings.MEDIA_URL)[1]
            RetailerAccount.objects.filter(id=instance.id).update(sLogo=db_file.replace(db_file.split(".")[0], str(instance.id)))
            os.remove(instance.sLogo.path)
    except (ValueError, FileNotFoundError) as e:
        pass