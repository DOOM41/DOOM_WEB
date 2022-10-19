from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    IntegerField
)
from transactions.models import Transactions


class TransSerializers(ModelSerializer):

    class Meta:
        model = Transactions
        field = '__all__'


class PaySerialize(Serializer):
    wallet_address = CharField(required=False)
    payment = IntegerField(required=False)

    class Meta:
        field = '__all__'