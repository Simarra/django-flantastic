from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Bakerie, Vote


@receiver(post_save, sender=Vote)
def signal_update_global_note(sender, instance=None, created=False, **kwargs):
    bakery = Bakerie.objects.get(id=instance.bakerie.id)
    bakery.update_global_note()
