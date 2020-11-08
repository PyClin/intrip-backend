from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import ClaimMappingCreate, WalletDeposit, WalletBalance, TicketList, TicketCreate, ClaimMoney, \
    TokenObtainPairView

urlpatterns = [
    path('', include('djoser.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_claim_mapping/', ClaimMappingCreate.as_view(), name="create_claim_mapping"),
    path('deposit/', WalletDeposit.as_view(), name="wallet_deposit"),
    path('balance/', WalletBalance.as_view(), name="wallet_balance"),
    path('ticket/list/', TicketList.as_view(), name="ticket_list"),
    path('ticket/create/', TicketCreate.as_view(), name="ticket_create"),
    path('claim/create/', ClaimMoney.as_view(), name="claim_money"),
]
