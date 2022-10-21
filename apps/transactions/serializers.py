from rest_framework.serializers import ModelSerializer
from transactions.models import (
    Transactions,
    BankAccount
)


class TransSerializers(ModelSerializer):

    class Meta:
        model = Transactions
        field = '__all__'


class BankAccountSerializers(ModelSerializer):

    class Meta:
        model = BankAccount
        field = '__all__'
