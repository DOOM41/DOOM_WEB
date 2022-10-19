from rest_framework.serializers import ModelSerializer
from transactions.models import Transactions


class TransSerializers(ModelSerializer):

    class Meta:
        model = Transactions
        field = '__all__'
