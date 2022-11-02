import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


class QrMixin:

    def qr_create(self, email):
        """Create Qr-s"""

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data('https://www.blockchain.com/ru/')


        QR_png = qr.make_image(
            image_factory=StyledPilImage, 
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(),
            embeded_image_path="staticfiles/qr/1.png"
        )

        QR_png.save(f'staticfiles/qr/QRcode_{email}.png')

        print('-------------------------------------')
        print('Qr code generating')
        print(f'QRcode_{email}.png')
        print('-------------------------------------')

