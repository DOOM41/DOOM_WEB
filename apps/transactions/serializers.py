from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    IntegerField,
    SlugRelatedField,
    HyperlinkedRelatedField
)

from transactions.models import Transactions
from bank_account.models import BankAccount
from bank_account.serializers import BankAccountClosedSerializer


class TransSendedSerializers(ModelSerializer):
    receiver = BankAccountClosedSerializer()
    status = CharField(required=False, read_only=False)
    amount = IntegerField(required=False, read_only=False)
    commission = IntegerField(required=False, read_only=False)

    class Meta:
        model = Transactions
        fields = (
            'receiver',
            'status',
            'amount',
            'commission',
        )

class TransGettedSerializers(ModelSerializer):
    sender = BankAccountClosedSerializer()
    status = CharField(required=False, read_only=False)
    amount = IntegerField(required=False, read_only=False)
    commission = IntegerField(required=False, read_only=False)

    class Meta:
        model = Transactions
        fields = (
            'sender',
            'status',
            'amount',
            'commission',
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

