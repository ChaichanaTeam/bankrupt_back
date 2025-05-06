from functools import wraps
from fastapi.responses import RedirectResponse
from typing import Any, Callable
from fastapi import HTTPException
from src.core.traceback import traceBack, TrackType
from src.core.config import settings
from enum import StrEnum

class AdminHTML():
    LOGIN: str = "admin/login.html"
    PANEL: str = "admin/panel.html"
    USERS: str = "admin/users.html"
    USERS_DETAILS: str = "admin/user_detail.html"

def template(template_name: str) -> Callable:
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request") or (args[0] if args else None)
            context: dict[str, Any] = {}
            used_template: str = template_name
            
            returned: dict[str, Any] | RedirectResponse | tuple[str, dict] | None = func(*args, **kwargs)

            if isinstance(returned, RedirectResponse):
                return returned

            if isinstance(returned, tuple):
                tpl, ctx = returned
                if isinstance(tpl, str) and isinstance(ctx, dict):
                    used_template = tpl
                    context.update(ctx)

            if isinstance(returned, dict):
                context.update(returned)
            
            context.update({"request": request})
            return settings.TEMPLATES.TemplateResponse(used_template, context)

        return wrapper
    return decorator