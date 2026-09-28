from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.core.context_processors import MENU_CACHE_KEY
from apps.core.models import MenuItem


@receiver([post_save, post_delete], sender=MenuItem)
def clear_menu_cache(sender, **kwargs):
    cache.delete(MENU_CACHE_KEY)
