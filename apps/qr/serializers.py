from rest_framework.serializers import (
    ModelSerializer,
)
from qr.models import QrModel


class QrSerializer(ModelSerializer):

    class Meta:
        model = QrModel
        fields = 'qr_png'