from typing import Any, Optional, Union
from rest_framework.response import Response
from auths.paginators import (
    AbstractPageNumberPaginator,
    AbstractLimitOffsetPaginator
)


class ResponseMixinAuth:
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

