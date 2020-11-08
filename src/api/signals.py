from django.dispatch import receiver, Signal
from djoser.signals import user_registered

from api.models import Wallet


# @receiver(user_registered)
# def user_registered_callback(sender, user, request, **kwargs):
#     print(f"Creating wallet for user: {user.id}")
#     Wallet.objects.create(
#         user=user
#     )
