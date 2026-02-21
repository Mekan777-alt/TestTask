from starlette.requests import Request
from starlette.responses import Response


def records_cache_key(
        func,
        namespace: str = "",
        request: Request = None,
        response: Response = None,
        args: tuple = None,
        kwargs: dict = None,
):
    metric_id = kwargs.get("metric_id")
    user = kwargs.get("current_user")
    return f"cache:records:{user.id}:{metric_id}"