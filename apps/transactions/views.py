#Django
from django.db.models import QuerySet

# Rest
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView

#Apps
from transactions.models import Transactions

#Serializer
from transactions.serializers import TransSerializers


class TransSet(
    ViewSet,
    ListAPIView
):
    queryset: QuerySet[Transactions] = Transactions.objects.all()
    serializer_class = TransSerializers


