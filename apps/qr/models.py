from django.db import models


class QrModel(models.Model):

    qr_png = models.ImageField(upload_to=None, max_length=100)

    class Meta:
        verbose_name = 'Qr'
        verbose_name_plural = 'Qr-s'
