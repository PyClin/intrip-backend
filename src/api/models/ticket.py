from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Ticket(models.Model):
    ticket_id = models.CharField(_("ticket id"), max_length=84, db_index=True)
    from_user = models.ForeignKey(get_user_model(), related_name="f_tickets", on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name="t_tickets", on_delete=models.CASCADE)
    txn_hash = models.CharField(_("Transaction hash"), max_length=84, db_index=True)
    timestamp = models.DateTimeField(_("Timestamp"), null=True, blank=True)
    destination = models.CharField(_("Destination"), max_length=100)
    source = models.CharField(_("Source"), max_length=100)
    amount = models.CharField(_("amount"), max_length=20)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True, db_index=True)

    def __str__(self):
        return f"{self.id}"
