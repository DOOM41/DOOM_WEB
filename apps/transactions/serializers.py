from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    IntegerField
)
from transactions.models import BankAccount
from transactions.models import Transactions


class TransSerializers(ModelSerializer):

    class Meta:
        model = Transactions
        field = '__all__'


class PaySerialize(Serializer):
    wallet_address = CharField(required=False)
    private_key = CharField(required=False)
    payment = IntegerField(required=False)

    class Meta:
        field = '__all__'

class BankAccountSerializers(ModelSerializer):

    class Meta:
        model = BankAccount
        field = '__all__'
