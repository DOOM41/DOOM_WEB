from typing import Any, Optional, Union

from django.db.models import QuerySet
from rest_framework.response import Response

from abstracts.validators import APIValidator
from auths.paginators import (
    AbstractPageNumberPaginator,
    AbstractLimitOffsetPaginator
)


class ResponseMixinBank:
    """ResponseMixin."""

    def get_json_response_bank(
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

class ValidationMixin:
    """ValidationMixin"""

    def get_obj_if_exists_raise_if_doesnt(
            self,
            queryset: QuerySet[Any],
            p_key: str
    ) -> None:

        obj: Any = queryset.get_obj(
            p_key
        )
        if not obj:
            raise APIValidator(
                f'Объект не найден {p_key}',
                'error',
                '404'
            )
        return obj


    def allow_delete_only_is_activated(
            self,
            queryset: QuerySet[Any],
            p_key: str
    ) -> Optional[tuple]:

        obj: Any = queryset.get_obj(
            p_key
        )

        if not obj:
            raise APIValidator(
                f'Объект не найден {p_key}',
                'error',
                '404'
            )

        if obj.is_activated:

            # obj.datetime_deleted = datetime.now()

            obj.delete()

            return (f'Объект удален: {obj.datetime_deleted}')

        return (f'Объект уже был удален {obj.datetime_deleted}')
