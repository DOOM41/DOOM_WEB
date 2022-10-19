#Django
from django.db.models import QuerySet

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

#Apps
from transactions.models import Transactions

#Serializer
from transactions.serializers import TransSerializers


class TransactionsViewSet(
    ModelViewSet,
    ListAPIView
):
    queryset: QuerySet[Transactions] = Transactions.objects.all()
    serializer_class = TransSerializers

    
