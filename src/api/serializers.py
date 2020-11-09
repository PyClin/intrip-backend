import traceback

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
    claimed_status = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Ticket
        fields = (
            'id',
            'ticket_id',
            'from_user',
            'to_user',
            'txn_hash',
            'source',
            'destination',
            'timestamp',
            'claimed_status',
            'amount',
        )

    def get_claimed_status(self, obj):
        try:
            status = obj.claims.claimed_status
            return status
        except Exception:
            print(traceback.format_exc())
            return ""


class TicketCreateSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], format="%Y-%m-%d %H:%M:%S")
    to_user = serializers.IntegerField(read_only=True, source="to_user.id")
    txn_hash = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'ticket_id',
            'from_user',
            'to_user',
            'txn_hash',
            'timestamp',
            'destination',
            'source',
            'amount'
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_type'] = self.user.user_type
        data['id'] = self.user.id
        data['username'] = self.user.username

        return data