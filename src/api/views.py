import traceback

from django.contrib.auth import get_user_model

from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.models import Wallet, Ticket, TicketClaimMapping
from api.serializers import TicketListSerializer, TicketCreateSerializer
from api.utils import GGHelper


class ClaimMappingCreate(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            employer_username = request.data.get("employer_username")
            User = get_user_model()
            try:
                employer = User.objects.get(username=employer_username)
            except User.DoesNotExist:
                employer = User.objects.create_user(
                    username=employer_username,
                    password="12ab34cd",
                    user_type=User.EMPLOYER
                )
                GGHelper().deposit(wallet_id=employer.wallet.id, amount=3000)
            try:
                wallet = Wallet.objects.get(user_id=user.id)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(
                    user=user
                )
                GGHelper().create_wallet(wallet_id=wallet.id, user_type=user.user_type)

            wallet.claim_from = employer.wallet
            wallet.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletDeposit(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            amount = request.data.get("amount")
            if not amount:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            wallet = user.wallet
            GGHelper().deposit(wallet_id=wallet.id, amount=amount)

            return Response(status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletBalance(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            wallet = user.wallet
            balance = GGHelper().wallet_balance(wallet.id)
            return Response(data={
                "balance": balance
            }, status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TicketList(ListCreateAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Ticket.objects.all()

    def filter_queryset(self, queryset):
        user = self.request.user
        return queryset.filter(from_user=user)

    def create(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TicketCreate(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer

    def perform_create(self, serializer):
        obj = serializer.save(from_user=self.request.user)
        return obj

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            ticket = self.perform_create(serializer)

            from_user = ticket.from_user
            claim_from_wallet = from_user.wallet.claim_from
            claim_from_user = claim_from_wallet.user

            if request.user.user_type == "employee":
                mapping = TicketClaimMapping.objects.create(
                    employer=claim_from_user,
                    ticket=ticket,
                    employee=request.user,
                    claimed_status=TicketClaimMapping.ELIGIBLE
                )
                print(f"Created TicketClaimMapping object")
                txn_hash = GGHelper().create_transaction(
                    from_wallet_id=from_user.wallet.id,
                    to_wallet_id=ticket.to_user.wallet.id,
                    amount=ticket.amount,
                    memo="",
                    employer_wallet_id=claim_from_wallet.id
                )
            else:
                mapping = TicketClaimMapping.objects.create(
                    employer=claim_from_user,
                    ticket=ticket,
                    employee=request.user,
                    claimed_status=TicketClaimMapping.NOT_ELIGIBLE
                )
                print(f"Created TicketClaimMapping object")
                txn_hash = GGHelper().create_transaction(
                    from_wallet_id=from_user.wallet.id,
                    to_wallet_id=ticket.to_user.wallet.id,
                    amount=ticket.amount,
                    memo="",
                )
            ticket.txn_hash = txn_hash
            ticket.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            raise
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClaimMoney(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            ids = data.get("ids")
            if not ids:
                return Response(data={
                    "err_msg": "ids field not present",
                }, status=status.HTTP_400_BAD_REQUEST)

            hashes = []
            for id in ids:
                ticket = Ticket.objects.get(id=id)
                ticket.claims.claimed_status = TicketClaimMapping.RAISED
                ticket.claims.save()

                hashes.append(ticket.txn_hash)
            print(f"All ticket ids status set to RAISED")
            amount = GGHelper().employee_claim(wallet_id=request.user.wallet.id, hashes=hashes)

            for id in ids:
                ticket = Ticket.objects.get(id=id)
                ticket.claims.claimed_status = TicketClaimMapping.SUCCESS
                ticket.claims.save()
            print(f"All ticket ids status set to SUCCESS")

            return Response(data={
                "amount": amount,
            }, status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
