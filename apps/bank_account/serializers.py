from rest_framework import serializers
from auths.models import CustomUser
from bank_account.models import BankAccount
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    IntegerField,
)


class BankAccountSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='id')
    address = serializers.CharField(required=False, read_only=False)
    balance = serializers.IntegerField(required=False, read_only=False)

    class Meta:
        model = BankAccount
        fields = (
            'owner',
            'address',
            'balance',
        )