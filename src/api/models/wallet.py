from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

import requests


class Wallet(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="wallet", on_delete=models.CASCADE)
    claim_from = models.ForeignKey("Wallet", related_name="claimants", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True, db_index=True)

    def __str__(self):
        return f"{self.id}"
