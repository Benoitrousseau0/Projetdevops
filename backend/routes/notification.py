from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.notification import get_notifications, mark_as_read, mark_all_as_read
from schemas.notification import NotificationOut
from utils.security import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationOut])
def lister_notifications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_notifications(db, current_user.id)

@router.post("/{notif_id}/lu", response_model=NotificationOut)
def marquer_lue(notif_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    notif = mark_as_read(db, notif_id, current_user.id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification introuvable ou accès refusé")
    return notif

@router.post("/lu-toutes")
def marquer_toutes_lues(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    mark_all_as_read(db, current_user.id)
    return {"message": "Toutes les notifications ont été marquées comme lues"}
