#Django
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

#Rest
from rest_framework.routers import DefaultRouter

#Apps
from apps.auths.views import UserViewSet
from apps.transactions.views import TransactionsViewSet
from apps.bank_account.views import BankAccountViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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

urlpatterns += [
    path(
        'api/v1/',
        include(router.urls)
    ),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'api/token/verify/', TokenVerifyView.as_view(), name='token_verify'
    ),
]
