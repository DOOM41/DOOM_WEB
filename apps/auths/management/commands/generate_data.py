from datetime import datetime
import random
import names
from auths.models import CustomUser
from django.contrib.auth.hashers import make_password

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Custom commands for generate data fo filling up database'

    # def __init__(self, *args, **kwargs):
    #     pass

    def _generate_password(self):
        """Generate number"""

        _number_from = 1000000000000000000000000
        _number_to = 9000000000000000000000000

        a = str(random.randint(
            _number_from,
            _number_to,)
        )

        list_a = [
            'jnbcrgqucjax',
            'eiwbfogcwegq23',
            'cqq793g2cnkjnwakoiweh',
            'wciunjeeeeeeemkajneube',
            'awkjejncwuy3kjcnawed',
            'cskjnliaeijiu2hdiuhsjen'
        ]

        return a + random.choice(list_a)

    def _generate_users(self):
        """Generate user/customuser objects"""

        TOTAL_USER_COUNT = 1

        def generate_email():
            _email_patterns: tuple = (
                'gmail.com', 'mail.ru',
                'yandex.ru', 'mail.ua',
                'inbox.ua', 'yahoo.com',
                'bk.ru'
            )
            return '{0}_{1}@{2}'.format(
                names.get_first_name().lower(),
                names.get_last_name().lower(),
                random.choice(_email_patterns)
            )


        def generate_phone_number():
            phone: str = '+7-'
            first_nums: str = ''
            sec_nums: str = ''
            third_nums: str = ''
            fifth_nums: str = ''

            for i in range(3):
                first_nums += str(random.randint(1, 9))
            for i in range(3):
                sec_nums += str(random.randint(1, 9))
            for i in range(2):
                third_nums += str(random.randint(1, 9))
            for i in range(2):
                fifth_nums += str(random.randint(1, 9))

            return phone + '{0}-{1}-{2}-{3}'.format(
                first_nums,
                sec_nums,
                third_nums,
                fifth_nums
            )

        def generate_pin():
            pin = ''
            for _ in range(5):
                pin += str(random.randint(0, 9))
            return pin

        # Generate superuser
        #
        if not CustomUser.objects.filter(is_superuser=True).exists():
            superuser: dict = {
                'is_superuser': True,
                'email': 'root@root.ru',
                'password': make_password('qwerty')
            }
            CustomUser.objects.create(**superuser)

        # Generate users
        #
        # if CustomUser.objects.filter(
        #     is_superuser=False
        # ).count() >= TOTAL_USER_COUNT:
        #     return


        _: int
        for _ in range(TOTAL_USER_COUNT):
            email = generate_email()
            login = generate_phone_number()
            pin = generate_pin()
            password = self._generate_password()

            custom_user: dict = {
                'email': email,
                'login': login,
                'verificated_code': pin,
                'password': password
            }
            CustomUser.objects.get_or_create(**custom_user)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling"""

        start: datetime = datetime.now()

        self._generate_users()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
