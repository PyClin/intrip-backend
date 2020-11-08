from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.models import Ticket


class TicketClaimMapping(models.Model):
    RAISED = "raised"
    VERIFIED = "verified"
    REJECTED = "rejected"
    SUCCESS = "success"
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not_eligible"
    CLAIMED_STATUS_CHOICES = [
        (RAISED, _("Raised")),
        (VERIFIED, _("Verified")),
        (REJECTED, _("Rejected")),
        (SUCCESS, _("Success")),
        (NOT_ELIGIBLE, _("Not Eligible")),
        (ELIGIBLE, _("Eligible")),
    ]
    employer = models.ForeignKey(get_user_model(), related_name="employer_claims", on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, related_name="claims", on_delete=models.CASCADE)
    employee = models.ForeignKey(get_user_model(), related_name="employee_claims", on_delete=models.CASCADE)
    claimed_status = models.CharField(_("Claimed Status"), max_length=32, choices=CLAIMED_STATUS_CHOICES)

    def __str__(self):
        return f"{self.id}"
