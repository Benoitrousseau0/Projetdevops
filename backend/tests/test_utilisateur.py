# backend/tests/test_utilisateur.py
#pytest -s tests/test_utilisateur.py

def test_inscription_utilisateur(client):
    response = client.post("/utilisateurs/", json={
        "nom": "user1",
        "email": "user1@mail.com",
        "mot_de_passe": "userpass",
        "role": "employe"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "user1@mail.com"

def test_email_deja_utilise(client):
    client.post("/utilisateurs/", json={
        "nom": "user2",
        "email": "user2@mail.com",
        "mot_de_passe": "pass",
        "role": "employe"
    })
    response = client.post("/utilisateurs/", json={
        "nom": "user2-bis",
        "email": "user2@mail.com",
        "mot_de_passe": "pass",
        "role": "employe"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email déjà utilisé"

def test_get_profil_connecte(client):
    # Crée un utilisateur
    client.post("/utilisateurs/", json={
        "nom": "user3",
        "email": "user3@mail.com",
        "mot_de_passe": "testpass",
        "role": "employe"
    })
    # Login
    login = client.post("/auth/token", data={
        "username": "user3@mail.com",
        "password": "testpass"
    })
    token = login.json()["access_token"]

    # Appelle /utilisateurs/moi avec le token
    response = client.get("/utilisateurs/moi", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "user3@mail.com"

def test_liste_utilisateurs_interdit_pour_employe(client):
    client.post("/utilisateurs/", json={
        "nom": "emp",
        "email": "emp@mail.com",
        "mot_de_passe": "emppass",
        "role": "employe"
    })
    login = client.post("/auth/token", data={
        "username": "emp@mail.com",
        "password": "emppass"
    })
    token = login.json()["access_token"]

    response = client.get("/utilisateurs/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 403
