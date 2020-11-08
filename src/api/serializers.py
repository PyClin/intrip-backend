import traceback

from rest_framework import serializers

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
    timestamp = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], format="%Y-%m-%d %H:%M:%S")
    from_user = serializers.CharField(read_only=True)
    txn_hash = serializers.CharField(read_only=True)

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