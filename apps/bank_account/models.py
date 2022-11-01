# django
from django.db import models
from django.db.models import (
    CharField,
    ForeignKey,
    PROTECT,
    QuerySet,
    IntegerField,
)
from settings.base import web3, MNEMONIC

#
from web3 import Account

# apps
from abstracts.models import AbstractsDateTime
from abstracts.mixins import PayMixin
from auths.models import CustomUser


class BankAccountQuerySet(PayMixin, QuerySet):

    def create_acc(self, user):
        acc, mnemonic = web3.eth.account.create_with_mnemonic()
        account: Account = Account.from_mnemonic(mnemonic)

        bank_address = '0x4bf9559C84690f153ed3874730F401893363c62c'
        wallet_address = account.address
        payment = 30

        own_account = web3.eth.account.from_mnemonic(MNEMONIC)
        private_key = own_account.privateKey
        transaction = self.build_txn(
            web3=web3,
            from_address=bank_address,
            to_address=wallet_address,
            amount=payment,
        )
        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key)
        txn_hash = web3.eth.sendRawTransaction(
            signed_txn.rawTransaction
        )
        balance = web3.eth.get_balance(account.address)
        acc_: 'BankAccount' = self.model(
            owner=user,
            address=account.address,
            private_key=account.privateKey.hex(),
            balance=str(balance),
        )
        acc_.save(using=self._db)
        return acc_


class BankAccount(AbstractsDateTime):
    owner: CustomUser = ForeignKey(
        CustomUser, related_name='Владелец', on_delete=PROTECT,
    )
    address: str = CharField(
        verbose_name="Адрес счета",
        max_length=200,
        unique=True,
        null=False,
    )
    private_key: str = CharField(
        verbose_name="Адрес счета",
        max_length=200,
        unique=True,
        null=False,
    )
    balance: int = CharField(
        verbose_name='Остаток',
        default=0,
        max_length=200,
    )
    count_of_transactions = IntegerField(
        verbose_name='Количество транзакций',
        default=0
    )

    objects = BankAccountQuerySet().as_manager()

    def __str__(self) -> str:
        return f'{self.owner.email}, {self.address}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
