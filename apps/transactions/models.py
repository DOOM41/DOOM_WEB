#django
from django.db.models import(
    CharField,
    IntegerField,
    ForeignKey,
    PROTECT,
    Model,
    TextChoices
)

#apps
from bank_account.models import BankAccount



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
        BankAccount, related_name="receiver_transactions", on_delete=PROTECT
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
    count_of_transactions = IntegerField(
        verbose_name='Количество транзакций',
        default=0
    )

    def __str__(self) -> str:
        return f'{self.sender}->{self.receiver}:{self.amount}'

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакций"

