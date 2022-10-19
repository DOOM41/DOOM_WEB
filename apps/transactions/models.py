from django.db.models import(
    CharField,
    IntegerField,
    ForeignKey,
    PROTECT,
    Model,
    TextChoices
)
from datetime import datetime, timedelta
from auths.models import CustomUser
from abstracts.models import AbstractsDateTime


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
    balance: int = IntegerField(
        verbose_name='Остаток',
        default=0,
    )

    def __str__(self) -> str:
        return f'{self.number}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"


class Transactions(Model):

    class StatusTransactions(TextChoices):
        PROCESSING = 'Обрабатывается'
        OK = 'Успешно'
        BAD = 'Неверно'
        LATE = 'Ожидание превышено'
        REJECTED = 'Отклонено'

    sender: BankAccount = ForeignKey(
        BankAccount, related_name="send_transactions", on_delete=PROTECT
    )
    receiver: BankAccount = ForeignKey(
        BankAccount, related_name="receiv_transactions", on_delete=PROTECT
    )
    status = CharField(
        verbose_name='Статус',
        max_length=18,
        choices=StatusTransactions.choices,
        default=StatusTransactions.PROCESSING
    )
    amount = IntegerField(
        verbose_name='Сумма перевода',
        null=False,
    )

    def __str__(self) -> str:
        return f'{self.sender}->{self.receiver}:{self.amount}'

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакций"


# class Card(models.Model):
#     account = models.ForeignKey(
#         BankAccount, related_name='cards', on_delete=models.PROTECT,
#     )
#     number = models.CharField(
#         verbose_name="Номер карты",
#         max_length=16,
#         unique=True,
#     )
#     cvv_code = models.CharField(
#         verbose_name="CVV2", max_length=3,
#     )
#     expiration_date = models.DateField(
#         verbose_name='Дата эксплуатации',
#         default=(datetime.now()+timedelta(365*3)),
#     )
#     balance = models.DecimalField(
#         verbose_name='Остаток',
#         default=0,
#         decimal_places=2,
#         max_digits=1000,
#     )
#
#     def __str__(self) -> str:
#         return self.number
#
#     class Meta:
#         verbose_name = "Карта"
#         verbose_name_plural = "Карты"
