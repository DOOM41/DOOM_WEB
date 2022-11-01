from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    IntegerField,
)
from transactions.models import Transactions



class TransSerializers(ModelSerializer):

    sender = CharField(required=False, read_only=False)
    receiver = CharField(required=False, read_only=False)
    status = CharField(required=False, read_only=False)
    amount = IntegerField(required=False, read_only=False)
    count_of_transactions = IntegerField(required=False, read_only=False)

    class Meta:
        model = Transactions
        fields = (
            'sender',
            'receiver',
            'status',
            'amount',
            'count_of_transactions',
        )


class PaySerialize(Serializer):
    payment = IntegerField(required=True)
    receiver = CharField(required=True, read_only=False)

    class Meta:
        field = '__all__'


class PinSerialize(Serializer):
    pin = CharField(required=True)

    class Meta:
        field = '__all__'