# django
from django.db.models import (
    CharField,
    IntegerField,
    ForeignKey,
    PROTECT,
    Model,
    TextChoices,
    QuerySet
)

# apps
from bank_account.models import BankAccount
from abstracts.mixins import SendEmailMixin
from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime


class TransactionsQuerySet(SendEmailMixin, QuerySet):

    def create_transaction(
        self,
        sender: BankAccount,
        receiver: BankAccount,
        amount: int,
        commission: int,
        sign,
    ):

        verificated_code = self.generate_pin()
        trans: 'BankAccount' = self.model(
            sender=sender,
            receiver=receiver,
            amount=amount,
            commission=commission,
            sender_sign=sign,
            verificated_code=verificated_code,
        )
        trans.save(using=self._db)
        self.send_message(verificated_code, sender.owner.email, 'trans')
        return trans

    def get_transaction(
        self,
        sender: BankAccount,
        pin,
    ):
        try:
            transaction: Transactions = self.get(
                sender=sender,
                status=Transactions.StatusTransactions.PROCESSING
            )
            if transaction.verificated_code != pin:
                raise APIValidator(
                    {'message': 'Неверные данные'}, field='Неверные данные', code='403')
            return transaction
        except Exception as e:
            raise APIValidator({'message': f'Транзакция не найдена'},
                               field='result', code='403')


class Transactions(AbstractsDateTime):

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
    sender_sign = CharField(
        verbose_name='Подпись отправителя.',
        max_length=255,
    )
    commission = IntegerField(
        verbose_name='Сумма комиссии',
        null=False,
    )
    verificated_code = CharField(
        'Код подтверждения',
        max_length=5,
        null=True
    )
    objects = TransactionsQuerySet().as_manager()

    def __str__(self) -> str:
        return f'{self.sender}->{self.receiver}:{self.amount}'

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакций"
