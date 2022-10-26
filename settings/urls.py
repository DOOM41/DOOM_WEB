#Django
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

#Rest
from rest_framework.routers import DefaultRouter

#Apps
from auths.views import UserViewSet
from transactions.views import TransactionsViewSet
from bank_account.views import BankAccountViewSet
# from transactions.views import BankAccountViewSet


urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
# ------------------------------------------------
# API-Endpoints
#
router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    'registration', UserViewSet
)
router.register(
    'transactions', TransactionsViewSet
)
router.register(
    'bank', BankAccountViewSet
)

urlpatterns += [
    path(
        'api/v1/',
        include(router.urls)
    ),
]
