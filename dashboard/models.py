from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
# Create your models here.

from django_extensions.db.models import TimeStampedModel

class Item(TimeStampedModel):

    location = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    identification = models.CharField(max_length=300, null=True, blank=True)
    tamper_seal = models.CharField(max_length=300, null=True, blank=True)
    overhead_sign = models.CharField(max_length=250)
    checklist  = models.CharField(max_length=250)
    s_on_floor  = models.CharField(max_length=250)
    comments   = models.CharField(max_length=1000, null=True, blank=True)
    inspected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return self.location
