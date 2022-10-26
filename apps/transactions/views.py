# Django
from django.db.models import QuerySet
from settings.conf import web3, MNEMONIC, ABI, my_contract_address

# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from transactions.models import (
    Transactions,
    BankAccount
)
from abstracts.mixins import PayMixin

# Serializer
from transactions.serializers import (
    TransSerializers, PaySerialize,
)

# Web 3
from web3 import Web3, Account
from hexbytes import HexBytes
from web3.contract import Contract
import json


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
    def get_contract(self, request: Request):
        serializer_class = PaySerialize
        my_address = '0x328A0e205c6d68cF76e0778f22bD747ec76B9159'
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
        txn = web3.eth.get_transaction(txn_hash.hex())
        txn_receipt = web3.eth.get_transaction_receipt(txn_hash.hex())
        my_t = {}
        for key, value in txn_receipt.items():
            try:
                if isinstance(value, HexBytes):
                    value: HexBytes
                    my_t[key] = value.hex()
                    continue
                my_t[key] = value
            except:
                continue
        return Response(data={
            'balance ether': my_t
        }, status=201)

    @action(
        methods=['post'],
        detail=False,
        url_path='pay-with-contract',
        permission_classes=(
            AllowAny,
        )
    )
    def pay_with_contract(self, request: Request):
        serializer_class = PaySerialize
        ERC20_ABI = json.loads(str(ABI))
        my_address = '0x328A0e205c6d68cF76e0778f22bD747ec76B9159'
        account = web3.eth.account.from_mnemonic(MNEMONIC)
        private_key = account.privateKey
        my_contract: Contract = web3.eth.contract(
            my_contract_address, abi=ERC20_ABI)
        dict_transaction = {
            'chainId': web3.eth.chain_id,
            'from': my_address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(my_address),
        }
        transaction = my_contract.functions.withdrawAll().buildTransaction(dict_transaction)
        signed_txn = web3.eth.account.signTransaction(transaction, private_key)

        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return Response(data={
            'balance ether': transaction
        }, status=201)

    @action(
        methods=['post'],
        detail=False,
        url_path='pay-for-item',
        permission_classes=(
            AllowAny,
        )
    )
    def pay_for_item(self, request: Request):
        serializer_class = PaySerialize
        ERC20_ABI = json.loads(str(ABI))
        wallet_address = request.data['wallet_address']
        private_key = request.data['private_key']
        pay = Web3.toWei(request.data['payment'], 'ether')

        my_contract: Contract = web3.eth.contract(
            my_contract_address, abi=ERC20_ABI)
        dict_transaction = {
            'chainId': web3.eth.chain_id,
            'from': wallet_address,
            'gasPrice': web3.eth.gas_price,
            'value': pay,
            'nonce': web3.eth.getTransactionCount(wallet_address),
        }
        transaction = my_contract.functions.payForItem().buildTransaction(dict_transaction)
        signed_txn = web3.eth.account.signTransaction(transaction, private_key)
        my_t = {}
        print(len(web3.eth.accounts))
        acc, mnemonic = web3.eth.account.create_with_mnemonic()
        account = Account.from_mnemonic(mnemonic)
        print(account.privateKey.hex())
        balance = web3.eth.get_balance(account.address)
        return Response(data={
            'balance ether': transaction,
            'pay': pay,
            'Комиссия': transaction['gas']*transaction['gasPrice'],
            'data': balance,
        }, status=201)
