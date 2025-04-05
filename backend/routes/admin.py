from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.ticket import get_tickets_by_status, get_avg_resolution_time_by_technician, get_critical_tickets
from models.utilisateur import RoleEnum
from utils.security import require_role
from crud.utilisateur import get_utilisateur_by_id, update_utilisateur_role
from schemas.utilisateur import UtilisateurOut, UpdateUserRoleRequest

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user=Depends(require_role([RoleEnum.admin]))):
    # 1. Nombre total de tickets ouverts/résolus
    tickets_opened = get_tickets_by_status(db, 'ouvert')
    tickets_resolved = get_tickets_by_status(db, 'resolu')

    # 2. Temps moyen de résolution par technicien
    avg_resolution_time_by_technician = get_avg_resolution_time_by_technician(db)

    # 3. Priorisation des tickets critiques
    critical_tickets = get_critical_tickets(db)

    return {
        "tickets_opened": len(tickets_opened),
        "tickets_resolved": len(tickets_resolved),
        "avg_resolution_time_by_technician": avg_resolution_time_by_technician,
        "critical_tickets": len(critical_tickets)
    }


@router.put("/utilisateurs/{user_id}", response_model=UtilisateurOut)
def update_user_role(
    user_id: int,
    update_request: UpdateUserRoleRequest,  # On récupère ici le corps de la requête
    db: Session = Depends(get_db),
    current_user=Depends(require_role([RoleEnum.admin]))
):
    utilisateur = get_utilisateur_by_id(db, user_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Mettre à jour le rôle de l'utilisateur
    utilisateur = update_utilisateur_role(db, user_id, update_request.new_role)

    return utilisateur