# Django
from django.db.models import QuerySet
from settings.conf import web3, MNEMONIC

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
# Apps
from transactions.models import Transactions
from abstracts.mixins import PayMixin

# Serializer
from transactions.serializers import TransSerializers, PaySerialize

# Web 3
from web3.middleware.geth_poa import geth_poa_middleware
from web3 import Web3
from hexbytes import HexBytes


class TransactionsViewSet(
    ModelViewSet,
    ListAPIView,
    PayMixin
):
    queryset: QuerySet[Transactions] = Transactions.objects.all()
    serializer_class = TransSerializers

    @action(
        methods=['post'],
        detail=False,
        url_path='pay-contract',
        permission_classes=(
            AllowAny,
        )
    )
    def get_ballance(self, request: Request):
        serializer_class = PaySerialize
        my_address = '0x79Ecbc0A1B3734707e2875Fc643336f3D96870dB'
        wallet_address = request.data['wallet_address']
        payment = request.data['payment']
        account = web3.eth.account.from_mnemonic(MNEMONIC)
        private_key = account.privateKey

        balance = web3.eth.get_balance(wallet_address)
        transaction = self.build_txn(
            web3=web3,
            from_address=my_address,
            to_address=wallet_address,
            amount=payment,
        )
        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key)
        txn_hash = web3.eth.sendRawTransaction(
            signed_txn.rawTransaction
        )
        # txn = web3.eth.get_transaction(txn_hash.hex())
        txn_receipt = web3.eth.get_transaction_receipt(txn_hash.hex())
        return Response(data={
            'balance ether': txn_receipt
        }, status=201)
