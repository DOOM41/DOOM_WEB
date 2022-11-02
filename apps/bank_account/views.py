# Django
import random
from typing import Any, Type
from django.db.models import QuerySet

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from auths.models import CustomUser
from transactions.models import (
    BankAccount
)
from bank_account.mixins import ResponseMixinBank, ValidationMixin
from auths.paginators import AbstractPageNumberPaginator

# Serializer
from bank_account.serializers import (
    BankAccountSerializer
)


class BankAccountViewSet(
    ResponseMixinBank,
    ValidationMixin,
    ModelViewSet,
    ListAPIView
):
    pass
    # queryset: QuerySet[BankAccount] = BankAccount.objects.all()
    # serializer_class = BankAccountSerializer
    # pagination_class: Type[AbstractPageNumberPaginator] = \
    #     AbstractPageNumberPaginator


    # def list(self, request: Request) -> Response:
    #     paginator: AbstractPageNumberPaginator = \
    #         self.pagination_class()

    #     objects: list[Any] = paginator.paginate_queryset(
    #         self.queryset,
    #         request
    #     )
    #     serializer: BankAccountSerializer = \
    #         BankAccountSerializer(
    #             objects,
    #             many=True
    #         )
    #     return self.get_json_response_bank(
    #         serializer.data,
    #         paginator
    #     )

    # def create(self, request: Request) -> Response:

    #     owner_count = CustomUser.objects.all().count()
    #     random_id = random.randint(1, owner_count)

    #     user: CustomUser = CustomUser.objects.get(id=random_id)

    #     count_owner: int = user.id
    #     address: str = '0xl' + str(
    #         random.randint(
    #             1000000000000000000000000000000,
    #             9000000000000000000000000000000
    #         )
    #     )
    #     balance: int = random.randint(100, 1_000_000)

    #     serializer: BankAccountSerializer = BankAccountSerializer(
    #         data={
    #             'owner': count_owner,
    #             'address': address,
    #             'balance': balance,
    #         }
    #     )
    #     if not serializer.is_valid(raise_exception=True):
    #         return self.get_json_response_bank(
    #             {
    #                 'message': 'Объект не был создан',
    #                 'payload': {
    #                     'user_id': count_owner,
    #                     'address': address,
    #                     'balance': balance,
    #                 }
    #             }
    #         )
    #     serializer.save()

    #     return self.get_json_response_bank(
    #         {
    #             'message': 'Объект был создан',
    #         }
    #     )

    # def partial_update(self, request: Request, pk: str) -> Response:

    #     obj: BankAccount = self.get_obj_if_exists_raise_if_doesnt(self.queryset, pk)

    #     serializer: BankAccountSerializer = \
    #         BankAccountSerializer(
    #             obj,
    #             data=request.data,
    #             partial=True
    #         )
    #     request.data['owner'] = obj.id

    #     if not serializer.is_valid():
    #         return self.get_json_response_bank(
    #             {
    #                 'message': 'Объект не был частично-обновлен',
    #                 'payload': request.data
    #             }
    #         )

    #     serializer.save()

    #     return self.get_json_response_bank(
    #         {
    #             'message': 'Объект был частично-обновлен',
    #             'payload': request.data
    #         }
    #     )

    # # @action(
    # #     methods=['post'],
    # #     detail=False,
    # #     url_path='open-bank-account',
    # #     permission_classes=(
    # #         AllowAny,
    # #     )
    # # )
    # # def open_bank_account(self):
    # #     a = random.randint(
    # #         1000000000000000000000000000000,
    # #         9000000000000000000000000000000
    # #     )
    # #
    # #     owner = 1
    # #     address = '0xl' + str(a)
    # #     balance = 0
    # #
    # #     BankAccount.objects.create(
    # #         owner, address, balance
    # #     )
    # #     return Response(status=201)
