from fastapi.testclient import TestClient

def creer_utilisateur_et_ticket(client: TestClient):
    # Création de l'utilisateur
    response_user = client.post("/utilisateurs/", json={
        "nom": "Jean",
        "email": "jean@mail.com",
        "mot_de_passe": "secret",
        "role": "employe"
    })
    assert response_user.status_code == 200
    user = response_user.json()

    # Login
    response_login = client.post("/auth/token", data={
        "username": "jean@mail.com",
        "password": "secret"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    # Création du ticket
    response_ticket = client.post("/tickets/", json={
        "titre": "Écran noir",
        "description": "Mon PC ne démarre plus"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response_ticket.status_code == 200
    ticket_id = response_ticket.json()["id"]

    return token, ticket_id


def test_ajout_commentaire(client):
    token, ticket_id = creer_utilisateur_et_ticket(client)

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
    token, ticket_id = creer_utilisateur_et_ticket(client)

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
