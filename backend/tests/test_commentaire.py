# tests/test_commentaire.py
# pytest -s tests/test_commentaire.py

from fastapi.testclient import TestClient
import uuid

def email_unique(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}@mail.com"

def creer_utilisateur_et_token(client: TestClient, nom: str, email: str, mot_de_passe: str, role: str = "employe"):
    # Obtenir un token admin pour créer un utilisateur
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    # Créer l'utilisateur avec les droits admin
    resp_creation = client.post("/utilisateurs/", json={
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": role
    }, headers=headers)
    print("Création utilisateur:", resp_creation.status_code, resp_creation.text)
    assert resp_creation.status_code == 200

    # Login
    resp = client.post("/auth/token", data={
        "username": email,
        "password": mot_de_passe
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print("Login utilisateur:", resp.status_code, resp.text)
    assert resp.status_code == 200
    return resp.json()["access_token"]

def creer_ticket(client: TestClient, token: str):
    resp = client.post("/tickets/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "titre": "Bug clavier",
        "description": "Touches bloquées",
        "priorite": "moyenne"
    })
    print("Création ticket:", resp.status_code, resp.text)
    assert resp.status_code == 200
    return resp.json()["id"]

def test_ajout_commentaire(client):
    email = email_unique("comment")
    token = creer_utilisateur_et_token(client, "Jean", email, "secret123", "employe")
    ticket_id = creer_ticket(client, token)

    resp = client.post("/commentaires/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "id_ticket": ticket_id,
        "contenu": "J’ai essayé de redémarrer, rien ne change."
    })

    print("Réponse ajout commentaire:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert data["contenu"] == "J’ai essayé de redémarrer, rien ne change."
    assert data["id_ticket"] == ticket_id

def test_liste_commentaires(client):
    email = email_unique("commentlist")
    token = creer_utilisateur_et_token(client, "Lise", email, "pass123", "employe")
    ticket_id = creer_ticket(client, token)

    # Ajout d’un commentaire
    client.post("/commentaires/", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "id_ticket": ticket_id,
        "contenu": "Test commentaire"
    })

    # Lecture des commentaires
    resp = client.get(f"/commentaires/ticket/{ticket_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    print("Réponse liste commentaires:", resp.status_code, resp.text)
    assert resp.status_code == 200
    commentaires = resp.json()
    assert isinstance(commentaires, list)
    assert any(c["contenu"] == "Test commentaire" for c in commentaires)

def test_suppression_commentaire_propre(client):
    email = email_unique("delcomment")
    token = creer_utilisateur_et_token(client, "User", email, "password123", "employe")
    ticket_id = creer_ticket(client, token)

    com = client.post("/commentaires/", headers={"Authorization": f"Bearer {token}"}, json={
        "id_ticket": ticket_id,
        "contenu": "A supprimer"
    }).json()

    delete = client.delete(
        f"/commentaires/ticket/{ticket_id}/commentaires/{com['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Suppression propre:", delete.status_code, delete.text)
    assert delete.status_code == 200
    assert delete.json()["message"] == "Commentaire supprimé avec succès"

def test_suppression_commentaire_interdit(client):
    email1 = email_unique("auteur")
    email2 = email_unique("intru")
    token1 = creer_utilisateur_et_token(client, "Auteur", email1, "abcdef", "employe")
    token2 = creer_utilisateur_et_token(client, "Intrus", email2, "ghijkl", "employe")
    ticket_id = creer_ticket(client, token1)

    com = client.post("/commentaires/", headers={"Authorization": f"Bearer {token1}"}, json={
        "id_ticket": ticket_id,
        "contenu": "Privé"
    }).json()

    delete = client.delete(
        f"/commentaires/ticket/{ticket_id}/commentaires/{com['id']}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    print("Suppression interdite:", delete.status_code, delete.text)
    assert delete.status_code == 403
    assert delete.json()["detail"] == "Suppression non autorisée"
