from django.shortcuts import render
from abstracts.models import AbstractsDateTime
from qr.mixins import QrMixin
from qr.models import QrModel
from qr.serializers import QrSerializer
from auths.paginators import AbstractPageNumberPaginator

class QrViewSet(
    AbstractsDateTime,
    QrMixin
):

    queryset = QrModel.objects.all()
    serializer_class = QrSerializer
    pagination_class = AbstractPageNumberPaginator

    def create(self, email):
        self.qr_create(email)
