#django
from django.db import models
from django.db.models import(
    CharField,
    IntegerField,
    ForeignKey,
    PROTECT,
)

#apps
from auths.models import CustomUser
from abstracts.models import AbstractsDateTime


class BankAccount(AbstractsDateTime):
    owner: ForeignKey = ForeignKey(
        CustomUser, related_name='Владелец', on_delete=PROTECT,
    )
    address: CharField = CharField(
        verbose_name="Адрес счета",
        max_length=200,
        unique=True,
        null=False,
    )
    balance: IntegerField = IntegerField(
        verbose_name='Остаток',
        default=0,
    )

    def __str__(self) -> str:
        return f'{self.address} | {self.balance}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
