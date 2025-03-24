from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from core.database import get_db
from fastapi.responses import JSONResponse
from sqlalchemy import text

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/", summary="Vérifie la connexion à la base de données")
def test_connexion(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return JSONResponse(content={"message": "connexion bdd marche ✅"})
    except OperationalError:
        return JSONResponse(status_code=500, content={"message": "connexion bdd échouée ❌"})
