from typing import Any, Callable, Optional

from starlette.requests import Request
from starlette.responses import Response


def records_cache_key(
        func: Callable[..., Any],
        namespace: str = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Optional[tuple[Any, ...]] = None,
        kwargs: Optional[dict[str, Any]] = None,
) -> str:
    metric_id = kwargs.get("metric_id") if kwargs else None
    user = kwargs.get("current_user") if kwargs else None
    user_id = user.id if user else 0
    return f"cache:records:{user_id}:{metric_id}"
