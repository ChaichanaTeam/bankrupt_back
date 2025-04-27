from fastapi import APIRouter, Depends, Request, Form, Cookie, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import UserLogin
from src.models.user import User
from src.db.dependencies import get_db
from src.db.queries import get_all_users, get_user_by_id, get_expired_users
from src.services.admin import AdminService
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.core.exceptions import user_not_found
from starlette.status import HTTP_302_FOUND
from typing import Optional
from src.core.traceback import traceBack, TrackType

router: APIRouter = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/login")
def admin_login_get(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request, "hide_nav": True, "error": None})

@router.post("/login")
def admin_login_post(request: Request,
                     email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin_login: UserLogin = UserLogin(email=email, password=password)

    try:
        token = AdminService.login(admin_login, db)
    except HTTPException:
        return templates.TemplateResponse("admin/login.html", {"request": request, "hide_nav": True, "error": "Invalid credentials"})
    except Exception as e:
        traceBack(f"{e}", type=TrackType.ERROR)
        return templates.TemplateResponse("admin/login.html", {"request": request, "hide_nav": True, "error": "Technical issues"})

    resp = RedirectResponse("/admin/panel", status_code=HTTP_302_FOUND)
    resp.set_cookie(key="admin_token", value=token, httponly=True)
    return resp

@router.get("/panel")
def admin_panel(request: Request,
                token: str = Cookie(None, alias="admin_token"), db: Session = Depends(get_db), deleted: Optional[int] = None):
    admin: User = AdminService.validate(token, db)

    return templates.TemplateResponse("admin/panel.html", {"request": request, "deleted": deleted, "user": admin})

@router.get("/users")
def admin_users(request: Request,
                token: str = Cookie(None, alias="admin_token"),
                db: Session = Depends(get_db)):
    try:
        AdminService.validate(token, db)
    except HTTPException:
        return templates.TemplateResponse("admin/login.html", {"request": request, "error": "Login again to continue"})
    
    users = get_all_users(db)
    unverified_users = get_expired_users(db)

    return templates.TemplateResponse("admin/users.html", {"request": request, "users": users, "unverified_users": unverified_users})

@router.post("/cleanup-unverified")
def cleanup_unverified_users(token: str = Cookie(None, alias="admin_token"),
                              db: Session = Depends(get_db)):
    AdminService.validate(token, db)

    expired_users = get_expired_users(db)
    deleted_count: int = len(expired_users)

    for user in expired_users:
        db.delete(user)
    db.commit()

    return RedirectResponse(f"/admin/panel?deleted={deleted_count}", status_code=HTTP_302_FOUND)

@router.get("/users/{user_id}")
def admin_user_detail(user_id: int, request: Request,
                      token: str = Cookie(None, alias="admin_token"),db: Session = Depends(get_db)):
    try:
        AdminService.validate(token, db)
    except HTTPException:
        return templates.TemplateResponse("admin/login.html", {"request": request, "error": "Login again to continue"})

    user = get_user_by_id(user_id, db)

    if not user:
        raise user_not_found

    return templates.TemplateResponse("admin/user_detail.html", {"request": request, "user": user})

@router.get("/logout")
def admin_logout():
    response = RedirectResponse(url="/admin/login")
    response.delete_cookie("admin_token")
    return response