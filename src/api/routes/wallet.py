# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from src.models.user import User
# from src.schemas.wallet import TransferRequest
# from src.db.dependencies import get_db
# from src.api.utils.auth import get_current_user
# from src.services.wallet import WalletService
#
# router: APIRouter = APIRouter()
#
# @router.post("/wallet/transfer")
# def transfer_money(transfer: TransferRequest,
#                    db: Session = Depends(get_db),
#                    user: User = Depends(get_current_user)):
#     WalletService.transfer_money_logic(transfer, db, user)
#
#     return {
#         "message": f"Transferred {transfer.amount} {transfer.to_email}"
#     }
#
# # @router.get("/wallet")
# def get_balance(user: Urer = Depends(get_current_user), db: Session = Depends(get_db)):
#     balance = WalletService.get_balance_logic(user, db)
#
#     return { "Balance": balance }
#
#
# @router.get("/wallet/history")
# def get_transfer_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     records = WalletService.get_transfer_history_logic(user, db)
#
#     return records