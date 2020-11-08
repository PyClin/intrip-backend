import traceback

from rest_framework import serializers

from api.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
    claimed_status = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(input_formats=["YYYY-mm-dd HH:MM:SS"], format="YYYY-mm-dd HH:MM:SS")

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
            'claimed_status'
        )

    def get_claimed_status(self, obj):
        try:
            status = obj.claims.claimed_status
            return status
        except Exception:
            print(traceback.format_exc())
            return ""


class TicketCreateSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(input_formats=["YYYY-mm-dd HH:MM:SS"], format="YYYY-mm-dd HH:MM:SS")

    class Meta:
        model = Ticket
        fields = (
            'ticket_id',
            'from_user',
            'to_user',
            'txn_hash',
            'timestamp',
            'destination',
            'source',
            'amount'
        )