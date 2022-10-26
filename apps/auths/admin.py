from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest

from auths.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        ('Information', {
            'fields': (
                'email',
                'password',
                'verificated_code',
                'login',
            )
        }),
        ('Permitions', {
            'fields': (
                'is_superuser',
                'is_staff',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
            ),
        }),
    )

    list_display = (
        'email',
        'is_staff',
        'verificated_code',
        'login',
    )
    search_fields = (
        'email',
    )
    list_filter = (
        'email',
        'is_superuser',
        'is_staff',
    )
    ordering = (
        'email',
    )

    def get_readonly_fields(
            self,
            request: WSGIRequest,
            obj: Optional[CustomUser] = None
    ) -> tuple:
        if not obj:
            return self.readonly_fields

        return self.readonly_fields


admin.site.register(CustomUser, CustomUserAdmin)
