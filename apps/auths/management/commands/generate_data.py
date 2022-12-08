#python
from datetime import datetime
import random
import names

#django
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

#apps
from bank_account.models import BankAccount
from auths.models import CustomUser


class Command(BaseCommand):
    help = 'Custom commands for generate data fo filling up database'

    # def __init__(self, *args, **kwargs):
    #     pass

    def _generate_users(self):
        """Generate user/customuser objects"""

        TOTAL_USER_COUNT = 2

        # Generate superuser
        #
        if not CustomUser.objects.filter(is_superuser=True).exists():
            superuser: dict = {
                'is_superuser': True,
                'email': 'root@root.ru',
                'password': make_password('qwerty')
            }
            CustomUser.objects.create(**superuser)
        so = {
            0:'',
            1:'.95'
        }
        for i in (0,1):
            user:CustomUser = CustomUser.objects.create(
                email=CustomUser.objects.normalize_email(f'duman.marat{so[i]}@mail.ru'),
                login=f'877593334{i}',
                password=make_password('DOOM41'),
                nick_name="DOOM41",
                verificated_code=None,
                is_active = True
            )
            BankAccount.objects.create_acc(user)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling"""

        start: datetime = datetime.now()

        self._generate_users()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
