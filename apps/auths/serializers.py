from rest_framework.serializers import (
    ModelSerializer,
)
from auths.models import CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'created_at',
            'email',
            'login',
            'avatar',
            'nick_name',
        ]
