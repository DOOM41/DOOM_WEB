# Python
from typing import Any, Type

# Django
from django.db.models import QuerySet

# Rest
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from abstracts.mixins import (
    SendEmailMixin,
    ResponseMixin,
    GenerateImageMixin
)
from abstracts.paginators import AbstractPageNumberPaginator
from auths.serializers import UserSerializer
from auths.models import CustomUser
from bank_account.models import BankAccount
from bank_account.serializers import BankAccountSerializer


class UserViewSet(
    SendEmailMixin,
    ModelViewSet,
    RetrieveUpdateAPIView,
    ResponseMixin,
    GenerateImageMixin
):
    queryset: QuerySet[CustomUser] = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class: Type[AbstractPageNumberPaginator] = \
        AbstractPageNumberPaginator

    def list(self, request: Request) -> Response:

        paginator: AbstractPageNumberPaginator = \
            self.pagination_class()

        objects: list[Any] = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: UserSerializer = \
            UserSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            paginator
        )

    def create(self, request: Request):
        login = request.data['login']
        email = request.data['email']
        password = 'qwerty'
        pin = self.generate_pin()
        user = CustomUser.objects.create_user(
            email, login, pin, password
        )
        self.send_message(pin, email, 'auths')
        return Response(data={
            'user id': f'id = {user.id}'
        }, status=201)

    @action(
        methods=['post'],
        detail=True,
        url_path='set-password',
        permission_classes=(
            AllowAny,
        )
    )
    def set_password(self, request: Request, pk):
        try:
            password = request.data['password']
            nick = request.data['nick']
            pin = request.data['pin']
        except:
            return Response(data={'message': 'Не хватает полей'}, status=401)
        user: CustomUser = CustomUser.objects.get_undeleted_user(
            id=pk
        )
        if not user.verificated_code:
            return Response(data={'message': 'Вы авторизованы'}, status=500)
        elif user.verificated_code != pin:
            return Response(data={'message': 'Неверный пин код'}, status=500)
        CustomUser.objects.set_user(user, nick, password)
        BankAccount.objects.create_acc(user)
        return Response(status=201)

    @action(
        methods=['get'],
        detail=False,
        url_path='get-me',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_me(self, request: Request):
        user: CustomUser = request.user
        serializer: UserSerializer = \
            UserSerializer(
                self.queryset.get(id=user.id)
            )
        bank_acc = BankAccount.objects.get(owner=user)
        bank_acc_ser: BankAccountSerializer = BankAccountSerializer(
            bank_acc
        )
        # try:
        #     user.nick_name = request.data['nick']
        #     user.save()
        # except:
        #     pass
        # self.generate_img_by_nickname(user)
        return Response(
            data={
                'user': serializer.data,
                'banc_acc': bank_acc_ser.data,
            },
            status=201
        )
    
    @action(
        methods=['post'],
        detail=False,
        url_path='generate-avatar',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def generate_avatar(self, request: Request):
        user: CustomUser = request.user
        serializer: UserSerializer = \
            UserSerializer(
                self.queryset.get(id=user.id)
            )
        user.nick_name = request.data['nick']
        user.save()
        self.generate_img_by_nickname(user)
        return Response(
            data={
                'user': serializer.data,
            },
            status=201
        )