from auths.models import CustomUser
from bank_account.models import BankAccount
from rest_framework.serializers import (
    SlugRelatedField,
    ModelSerializer,
    CharField,
    IntegerField,
)


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'login',
        )


class BankAccountSerializer(ModelSerializer):
    owner = UserSerializer()
    address = CharField(required=False, read_only=False)
    balance = IntegerField(required=False, read_only=False)

    class Meta:
        model = BankAccount
        fields = (
            'owner',
            'address',
            'balance',
        )


class BankAccountClosedSerializer(ModelSerializer):
    owner = UserSerializer()
    address = CharField(required=False, read_only=False)

    class Meta:
        model = BankAccount
        fields = (
            'owner',
            'address',
        )