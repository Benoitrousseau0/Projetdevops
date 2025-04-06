# backend/tests/test_ticket.py
# pytest -s tests/test_ticket.py

from fastapi.testclient import TestClient

def creer_utilisateur_et_token(client: TestClient, email: str, mot_de_passe: str, role="employe") -> str:
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    client.post("/utilisateurs/", json={
        "nom": "temp",
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": role
    }, headers=headers)

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
        "priorite": "elevee"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Problème VPN"
    assert data["priorite"] == "elevee"
    assert data["statut"] == "ouvert"

def test_assignation_par_admin(client: TestClient):
    emp_token = creer_utilisateur_et_token(client, "emp@mail.com", "emp123", "employe")

    resp = client.post("/tickets/", headers={"Authorization": f"Bearer {emp_token}"}, json={
        "titre": "Écran noir",
        "description": "Écran ne s'allume plus.",
        "priorite": "critique"
    })
    assert resp.status_code == 200
    ticket_id = resp.json()["id"]

    tech = client.post("/tests/create-technicien").json()
    admin = client.post("/tests/create-admin").json()

    assign = client.post(f"/tickets/{ticket_id}/assigner", headers={
        "Authorization": f"Bearer {admin['token']}"
    }, json=[tech["id"]])

    assert assign.status_code == 200
    assert assign.json()["message"] == "Techniciens assignés avec succès"

def test_update_ticket_interdit_pour_autre_employe(client: TestClient):
    token1 = creer_utilisateur_et_token(client, "u1@mail.com", "123456", "employe")
    token2 = creer_utilisateur_et_token(client, "u2@mail.com", "654321", "employe")

    ticket = client.post("/tickets/", headers={"Authorization": f"Bearer {token1}"}, json={
        "titre": "Souris cassée",
        "description": "La souris ne bouge plus.",
        "priorite": "faible"
    }).json()

    update = client.put(f"/tickets/{ticket['id']}", headers={"Authorization": f"Bearer {token2}"}, json={
        "titre": "Souris ok",
        "description": "Test update",
        "priorite": "faible",
        "statut": "ouvert"
    })

    assert update.status_code == 403

def test_suppression_ticket_employe_si_ouvert(client: TestClient):
    token = creer_utilisateur_et_token(client, "suppemp@mail.com", "emp123", "employe")

    # Création du ticket
    creation = client.post("/tickets/", headers={"Authorization": f"Bearer {token}"}, json={
        "titre": "À supprimer",
        "description": "Ce ticket sera supprimé",
        "priorite": "moyenne"
    })
    assert creation.status_code == 200
    ticket = creation.json()
    ticket_id = ticket["id"]

    # 🔍 Vérifie bien que c'est lui l'auteur
    info = client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {token}"})
    assert info.status_code == 200
    assert info.json()["id"] == ticket_id

    # Suppression
    suppression = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {token}"})
    assert suppression.status_code == 200
    assert suppression.json()["message"] == "Ticket supprimé avec succès"

def test_suppression_ticket_refuse_si_non_ouvert(client: TestClient):
    token = creer_utilisateur_et_token(client, "employe2@mail.com", "abcabc", "employe")

    # Création d’un ticket
    resp = client.post("/tickets/", headers={"Authorization": f"Bearer {token}"}, json={
        "titre": "Fermé",
        "description": "Ce ticket va être mis à jour.",
        "priorite": "faible"
    })
    assert resp.status_code == 200
    ticket = resp.json()
    ticket_id = ticket["id"]

    # Mise à jour du statut à "fermé"
    update = client.put(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {token}"}, json={
        "titre": "Fermé",
        "description": "Mise à jour du statut",
        "priorite": "faible",
        "statut": "ferme"
    })
    assert update.status_code == 200

    # Tentative de suppression refusée
    delete = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete.status_code == 403
    assert delete.json()["detail"] == "Seuls les tickets ouverts peuvent être supprimés par leur auteur"

def test_suppression_ticket_par_admin(client: TestClient):
    emp_token = creer_utilisateur_et_token(client, "employe3@mail.com", "abcabc", "employe")
    admin = client.post("/tests/create-admin").json()

    resp = client.post("/tickets/", headers={"Authorization": f"Bearer {emp_token}"}, json={
        "titre": "À supprimer par admin",
        "description": "Admin peut tout faire",
        "priorite": "critique"
    })
    ticket_id = resp.json()["id"]

    deletion = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {admin['token']}"})
    assert deletion.status_code == 200

def test_filtrage_tickets(client: TestClient):
    token = creer_utilisateur_et_token(client, "filtre@mail.com", "passpass", "employe")

    for prio in ["faible", "elevee"]:
        client.post("/tickets/", headers={"Authorization": f"Bearer {token}"}, json={
            "titre": f"Test {prio}",
            "description": "Pour le filtrage",
            "priorite": prio
        })

    resp = client.get("/tickets/?priorite=elevee", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    tickets = resp.json()
    assert all(t["priorite"] == "elevee" for t in tickets)
