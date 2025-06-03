from fastapi import APIRouter, Depends, Request, Form, Cookie, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import UserLogin
from src.models.user import User
from src.db.dependencies import get_db
from src.db.queries import get_all_users, get_user_by_id, get_expired_users
from src.services.admin import AdminService
from src.api.utils.auth import get_current_user_cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.core.exceptions import user_not_found
from starlette.status import HTTP_302_FOUND
from typing import Any
from src.core.templates import template, AdminHTML
from src.core.config import settings
from src.core.traceback import traceBack, TrackType

router: APIRouter = APIRouter()

@router.get("/")
@template(None)
def admin_redirect(request: Request):
    return (AdminHTML.LOGIN, {"hide_nav": True, "error": None})

@router.get("/login")
@template(AdminHTML.LOGIN)
def admin_login_gui(request: Request) -> dict[str, Any]:
    return {"hide_nav": True, "error": None}

@router.post("/login")
@template(AdminHTML.LOGIN)
def admin_login_form(request: Request,
                     email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin_login: UserLogin = UserLogin(email=email, password=password)

    try:
        token = AdminService.login(admin_login, db)
    except HTTPException as e:
        return (AdminHTML.LOGIN, {"hide_nav": True, "error": f"{e.detail}"})
    except Exception as e:
        traceBack(f"{e}", type=TrackType.ERROR)
        return ("admin/login.html", {"request": request, "hide_nav": True, "error": "Technical issues"})

    resp = RedirectResponse(url="/admin/panel", status_code=HTTP_302_FOUND)
    resp.set_cookie(key="admin_token", value=token, httponly=True)
    return resp

@router.get("/panel")
@template(AdminHTML.PANEL)
def admin_panel(request: Request,
                admin: User = Depends(get_current_user_cookie), db: Session = Depends(get_db),
                deleted: int | None = None):
    try:
        AdminService.validate(admin)
    except HTTPException as e:
        return (AdminHTML.LOGIN, {"hide_nav": True, "error": f"{e.detail}"})
    
    return {"deleted": deleted, "email": admin.email}

@router.get("/users")
@template(AdminHTML.USERS)
def admin_users(request: Request,
                admin: User = Depends(get_current_user_cookie),
                db: Session = Depends(get_db)):
    try:
        AdminService.validate(admin)
    except HTTPException as e:
        return (AdminHTML.LOGIN, {"hide_nav": True, "error": f"{e.detail}"})

    users = get_all_users(db)
    unverified_users = get_expired_users(db)

    return {"users": users, "unverified_users": unverified_users}

@router.post("/cleanup-unverified")
def cleanup_unverified_users(request: Request,
                              admin: User = Depends(get_current_user_cookie),
                              db: Session = Depends(get_db)):
    try:
        AdminService.validate(admin)
    except HTTPException as e:
        return (AdminHTML.LOGIN, {"hide_nav": True, "error": f"{e.detail}"})

    deleted_count: int = AdminService.cleanup_users(db)

    return RedirectResponse(f"/admin/panel?deleted={deleted_count}", status_code=HTTP_302_FOUND)

@router.get("/users/{user_id}")
@template(AdminHTML.USERS_DETAILS)
def admin_user_detail(user_id: int, request: Request,
                      admin: User = Depends(get_current_user_cookie),db: Session = Depends(get_db)):
    try:
        AdminService.validate(admin)
    except HTTPException as e:
        return (AdminHTML.LOGIN, {"hide_nav": True, "error": f"{e.detail}"})
    
    user = get_user_by_id(user_id, db)

    if not user:
        raise user_not_found

    return {"user": user}

@router.get("/logout")
def admin_logout():
    response = RedirectResponse(url="/admin/login")
    response.delete_cookie("authorization")
    return response