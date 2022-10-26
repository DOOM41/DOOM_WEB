# Django
from typing import Any, Type

from django.db.models import QuerySet

# Rest
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from abstracts.mixins import SendEmailMixin
from auths.mixins import ResponseMixinAuth
from auths.paginators import AbstractPageNumberPaginator
from auths.serializers import UserSerializer
from auths.models import CustomUser




class UserViewSet(
    SendEmailMixin,
    ResponseMixinAuth,
    ModelViewSet,
    RetrieveAPIView,
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
        CustomUser.objects.create_user(
            email, login, pin, password
        )


    @action(
        methods=['post'],
        detail=False,
        url_path='set-password',
        permission_classes=(
            AllowAny,
        )
    )
    def set_password(self, request: Request):
        try:
            email = request.data['email']
            password = request.data['password']
            pin = request.data['pin']
        except:
            return Response(data={'message': 'Не хватает полей'}, status=401)
        user: CustomUser = CustomUser.objects.get_undeleted_user(
            email=email
        )
        if not user.verificated_code:
            return Response(data={'message': 'Вы авторизованы'}, status=500)
        elif user.verificated_code != pin:
            return Response(data={'message': 'Неверный пин код'}, status=500)
        user.verificated_code = None
        user.set_password(password)
        user.save()
        return Response(status=201)

    def retrieve(self, request: Request, pk: str):
        try:
            serializer: UserSerializer = \
                UserSerializer(
                    self.queryset.get(id=pk)
                )
        except:
            return Response(
                data={'message': 'Такой пользователь не найден'},
                status=404
            )
        return Response(
            data=serializer.data,
            status=201
        )
