# Django
import random
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
from web3 import Web3
from hexbytes import HexBytes
from attributedict.collections import AttributeDict
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
        txn_receipt: AttributeDict = web3.eth.get_transaction_receipt(
            txn_hash.hex())
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
        # # wallet_address = request.data['wallet_address']
        # # payment = request.data['payment']
        # my_address = '0x328A0e205c6d68cF76e0778f22bD747ec76B9159'
        # account = web3.eth.account.from_mnemonic(MNEMONIC)
        # private_key = account.privateKey
        # # balance = web3.eth.get_balance(wallet_address)
        ERC20_ABI = json.loads('''[
	{
		"inputs": [],
		"name": "payForItem",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "targetAddr",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferTo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "withdrawAll",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "payments",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]''')
        my_contract_address = '0x66B7ac8172a58558271ea600f419059EAf245BB8'
        my_contract: Contract = web3.eth.contract(
            my_contract_address, abi=ERC20_ABI)
        all_functions = my_contract.all_functions()
        print(all_functions)
        wallet_address = request.data['wallet_address']
        payment = request.data['payment']
        balance_of_token = my_contract.functions
        return Response(data={
            'balance ether': balance_of_token
        }, status=201)



