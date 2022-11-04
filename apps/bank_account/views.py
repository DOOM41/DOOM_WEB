# Django
import random
from typing import Any, Type
from django.db.models import QuerySet

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

# Apps
from auths.models import CustomUser
from bank_account.models import (
    BankAccount
)
from transactions.models import Transactions
from transactions.serializers import (
    TransSendedSerializers, 
    TransGettedSerializers
)
from abstracts.mixins import ResponseMixin
from abstracts.paginators import (
    AbstractPageNumberPaginator,
)

# Serializer
from bank_account.serializers import (
    BankAccountSerializer
)


class BankAccountViewSet(
    ModelViewSet,
    ListAPIView,
    ResponseMixin
):
    queryset: QuerySet[CustomUser] = BankAccount.objects.all()
    serializer_class = BankAccount
    pagination_class: Type[AbstractPageNumberPaginator] = \
        AbstractPageNumberPaginator

    @action(
        methods=['get'],
        detail=False,
        url_path='get-my-transactions',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_my_sended_transactions(self, request: Request):
        bank_acc = self.queryset.get(owner=request.user)
        pagination_class = self.pagination_class()
        transactions_sended: Transactions = \
            Transactions.objects.filter(sender=bank_acc)
        trans_sended = TransSendedSerializers(transactions_sended, many=True)
        return self.get_json_response(
            data=trans_sended.data, 
            paginator=pagination_class
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='get-my-transactions',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_my_getted_transactions(self, request: Request):
        bank_acc = self.queryset.get(owner=request.user)
        pagination_class = self.pagination_class()
        transactions_getted: Transactions = \
            Transactions.objects.filter(receiver=bank_acc)
        trans_getted = TransSendedSerializers(transactions_getted, many=True)
        return self.get_json_response(
            data=trans_getted.data, 
            paginator=pagination_class
        )
