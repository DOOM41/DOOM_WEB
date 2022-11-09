# Django
from django.db.models import QuerySet
from settings.conf import web3

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from abstracts.validators import APIValidator
from transactions.models import (
    Transactions,
    BankAccount
)
from transactions.serializers import PinSerialize
from auths.models import CustomUser
from abstracts.mixins import PayMixin

# Serializer
from transactions.serializers import (
    TransSendedSerializers, PaySerialize,
)

# Web 3
from eth_account.datastructures import (
    SignedTransaction,
)

class TransactionsViewSet(
    ModelViewSet,
    ListAPIView,
    PayMixin,
):
    queryset: QuerySet[Transactions] = Transactions.objects.all()
    serializer_class = TransSendedSerializers

    @action(
        methods=['post'],
        detail=False,
        url_path='make-transaction',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def make_transaction(self, request: Request):
        serializer_class = PaySerialize
        # GET users data
        sender: CustomUser = request.user
        email = request.data['email']
        reciever = CustomUser.objects.get_undeleted_user(email)
        amount = request.data['payment']

        # GET Bank acc
        sender_wallet: BankAccount = \
            BankAccount.objects.get(owner=sender)
        reciever_wallet: BankAccount = \
            BankAccount.objects.get(owner=reciever)

        # GET sign
        private_key = web3.toHex(hexstr=sender_wallet.private_key)
        transaction = self.build_txn(
            web3=web3,
            from_address=sender_wallet.address,
            to_address=reciever_wallet.address,
            amount=amount,
        )
        signed_txn: SignedTransaction = web3.eth.account.sign_transaction(
            transaction, private_key
        )
        Transactions.objects.create_transaction(
            sender=sender_wallet,
            receiver=reciever_wallet,
            amount=amount,
            commission=transaction['gasPrice']**2,
            sign=signed_txn.rawTransaction.hex(),
        )
        return Response(transaction['gasPrice']**2, status=201)

    @action(
        methods=['post'],
        detail=False,
        url_path='approve-transaction',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def approve_transaction(self, request: Request):
        serializer_class = PinSerialize
        # Get user Acc
        sender: BankAccount = \
            BankAccount.objects.get(owner=request.user)
        pin = request.data['pin']

        # Get transation
        transation: Transactions = Transactions.objects.get_transaction(
            sender=sender, pin=pin)
        sign = web3.toHex(hexstr=transation.sender_sign)

        # Make transaction
        txn_hash = web3.eth.sendRawTransaction(sign)
        txn = web3.eth.get_transaction(txn_hash.hex())
        txn_receipt = web3.eth.get_transaction_receipt(txn_hash.hex())
        balance = web3.eth.get_balance(sender.address)
        transation.status = Transactions.StatusTransactions.OK
        transation.save()
        my_t = self.build_txn_for_user(txn_receipt,transation.sender,transation.receiver)
        return Response(my_t, status=201)
