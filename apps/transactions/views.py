#Django
import random
from django.db.models import QuerySet

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

#Apps
from transactions.models import (
    Transactions,
    BankAccount
)

#Serializer
from transactions.serializers import (
    TransSerializers,
    BankAccountSerializers
)


class TransactionsViewSet(
    ModelViewSet,
    ListAPIView
):
    queryset: QuerySet[Transactions] = Transactions.objects.all()
    serializer_class = TransSerializers



class BankAccountViewSet(
    ModelViewSet,
    ListAPIView
):
    queryset: QuerySet[BankAccount] = BankAccount.objects.all()
    serializer_class = BankAccountSerializers


    @action(
        methods=['post'],
        detail=False,
        url_path='open-bank-account',
        permission_classes=(
                AllowAny,
        )
    )
    def open_bank_account(self, request: Request):
        a = random.randint(
            1000000000000000000000000000000,
            9000000000000000000000000000000
        )

        owner = request.data['id']
        address = '0xl' + str(a)
        balance = 0

        BankAccount.objects.create(
            owner, address, balance
        )
        return Response(status=201)


    
