# backend/tests/test_ticket.py
# pytest -s tests/test_ticket.py

from fastapi.testclient import TestClient


def creer_utilisateur_et_token(client: TestClient, email: str, mot_de_passe: str, role="employe") -> str:
    client.post("/utilisateurs/", json={
        "nom": "temp",
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": role
    })
    resp = client.post("/auth/token", data={
        "username": email,
        "password": mot_de_passe
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_creation_ticket_par_employe(client: TestClient):
    token = creer_utilisateur_et_token(client, "ticketuser@mail.com", "abc123", "employe")
    response = client.post("/tickets/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "titre": "Problème VPN",
        "description": "Impossible de se connecter.",
        "priorite": "Élevée"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Problème VPN"
    assert data["priorite"] == "Élevée"
    assert data["statut"] == "Ouvert"


def test_assignation_par_admin(client: TestClient):
    # Employé + création ticket
    emp_token = creer_utilisateur_et_token(client, "emp@mail.com", "emp123", "employe")

    resp = client.post("/tickets/", headers={
        "Authorization": f"Bearer {emp_token}"
    }, json={
        "titre": "Écran noir",
        "description": "Écran ne s'allume plus.",
        "priorite": "Critique"
    })
    assert resp.status_code == 200
    ticket_id = resp.json()["id"]

    # Technicien
    client.post("/utilisateurs/", json={
        "nom": "tech",
        "email": "tech@mail.com",
        "mot_de_passe": "tech123",
        "role": "technicien"
    })

    # Admin
    admin_token = creer_utilisateur_et_token(client, "admin@mail.com", "admin123", "admin")

    # Assigner le ticket
    assign = client.post(f"/tickets/{ticket_id}/assigner", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=[2])  # ✅ liste directe demandée par la route

    assert assign.status_code == 200
    assert assign.json()["message"] == "Techniciens assignés avec succès"


def test_update_ticket_interdit_pour_autre_employe(client: TestClient):
    # Deux employés
    token1 = creer_utilisateur_et_token(client, "u1@mail.com", "123", "employe")
    token2 = creer_utilisateur_et_token(client, "u2@mail.com", "456", "employe")

    # u1 crée le ticket
    ticket = client.post("/tickets/", headers={
        "Authorization": f"Bearer {token1}"
    }, json={
        "titre": "Souris cassée",
        "description": "La souris ne bouge plus.",
        "priorite": "Faible"
    }).json()

    # u2 tente de modifier
    update = client.put(f"/tickets/{ticket['id']}", headers={
        "Authorization": f"Bearer {token2}"
    }, json={
        "titre": "Souris ok",
        "description": "Test update",
        "priorite": "Faible",
        "statut": "Ouvert"
    })

    assert update.status_code == 403


