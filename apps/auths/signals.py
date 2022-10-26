# Python
import time
from typing import Any
import pyqrcode
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

# Django
from art import tprint
from django.db.models.base import ModelBase
from django.db.models.signals import (
    post_delete,
    post_save,
    pre_delete,
    pre_save
)
from django.dispatch import receiver

# Apps
from auths.models import CustomUser


@receiver(
    post_save,
    sender=CustomUser
)
def post_save_tempModel(
    sender: ModelBase,
    instance: CustomUser,
    **kwargs: Any
) -> None:
    """Signal post-save TempModel."""

    # code = pyqrcode.create('Hello. Uhh, can we have your liver?')
    # code.svg('live-organ-transplants.svg', 3.6)
    # code.svg('live-organ-transplants.svg', scale=1, module_color='black', background='white', quiet_zone=1)


    logo = Image.open('staticfiles/qr/15.png')

    basewidth = 100

    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    QRcode = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )

    QRcode.add_data('https://www.blockchain.com/ru/')

    QRcode.make()

    QRimg = QRcode.make_image(
        fill_color='black', back_color="white").convert('RGB')

    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    QRimg.save(f'staticfiles/qr/QR_{instance.id}.png')

    print('QR code generated!')

    tprint('!!! POST_SAVE called !!!')
    print(f'!!!{instance.id}!!!')
