#Python
from typing import Any, Optional, Union
import random

#Django
from django.core.mail import send_mail
from settings.base import EMAIL_HOST_USER

#Rest
from rest_framework.response import Response

#Apps
from abstracts.validators import APIValidator
from auths.paginators import (
    AbstractPageNumberPaginator,
    AbstractLimitOffsetPaginator
)
from web3 import Web3

class ResponseMixin:
    """ResponseMixin."""
    def get_json_response(
        self,
        data: dict[Any, Any],
        paginator: Optional[
            Union[
                AbstractPageNumberPaginator,
                AbstractLimitOffsetPaginator
            ]
        ] = None
    ) -> Response:

        if paginator:
            return paginator.get_paginated_response(
                data
            )
        return Response(
            {
                'results': data
            }
        )


class PayMixin:
    def build_txn(
            self,
            *,
            web3: Web3,
            from_address: str,
            to_address: str,
            amount: float,  
        ) -> dict[str, int | str]:
        gas_price = web3.eth.gas_price
        
        gas = 2_000_000

        nonce = web3.eth.getTransactionCount(from_address)

        txn = {
            'chainId': web3.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': int(Web3.toWei(amount, 'ether')),
            'nonce': nonce, 
            'gasPrice': gas_price,
            'gas': gas,
        }
        return txn


class SendEmailMixin:
    """NotificationMixin."""
    def generate_pin(self):
        pin = ''
        for _ in range(5):
            pin += str(random.randint(0, 9))
        return pin

    def send_to_authentifacate(self, pin, user_email: str) -> str:
        try:
            send_mail(
                f'Здравствуйте, {user_email}',
                f"Введите этот пин-код, чтобы подтвердить вашу почту: {pin}",
                EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
            )
        except Exception as e:
            raise APIValidator(
                f'Ошибка отправки {e}',
                'error',
                '500',
            )
