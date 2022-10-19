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
]
