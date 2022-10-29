from rest_framework.serializers import (
    ModelSerializer,
)
from auths.models import CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
