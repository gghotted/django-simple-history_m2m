from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from simple_history.manager import HistoryManager


def has_history(model):
    history = getattr(model, 'history', None)
    return history and isinstance(history, HistoryManager)


@receiver(m2m_changed)
def track_m2m_field(sender, instance, reverse, **kwargs):
    if has_history(instance) and not reverse:
        for f in instance._meta.many_to_many:
            m2m = getattr(instance, f.name)
            json_value = list(m2m.values_list('id', flat=True))
            setattr(instance, '%s_list' % f.name, json_value)
        instance.save()

    

    