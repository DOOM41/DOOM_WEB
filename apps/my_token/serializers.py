from rest_framework.serializers import (
    Serializer,
    CharField
)


class PinSerialize(Serializer):
    abi = CharField(required=True)

    class Meta:
        field = '__all__'

