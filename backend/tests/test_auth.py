# backend/tests/test_auth.py
# pytest -s tests/test_auth.py

import time
from datetime import timedelta
from jose import jwt
from utils.security import create_access_token


def creer_utilisateur(client, nom, email, mot_de_passe):
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}
    resp = client.post("/utilisateurs/", json={
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": "employe"
    }, headers=headers)
    assert resp.status_code == 200, f"Erreur création utilisateur : {resp.text}"


def test_login_succes(client):
    email = "test@mail.com"
    creer_utilisateur(client, "testuser", email, "secret")

    response = client.post("/auth/token", data={
        "username": email,
        "password": "secret"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    print("Réponse login:", response.status_code, response.text)
    assert response.status_code == 200, f"Échec login : {response.text}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_echec(client):
    email = "wrong@mail.com"
    creer_utilisateur(client, "wrongpass", email, "abc123")

    response = client.post("/auth/token", data={
        "username": email,
        "password": "incorrect"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"


def test_trop_de_tentatives(client):
    email = "ratelimit@mail.com"
    creer_utilisateur(client, "ratelimit", email, "test123")

    for _ in range(5):
        client.post("/auth/token", data={
            "username": email,
            "password": "wrongpass"
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    response = client.post("/auth/token", data={
        "username": email,
        "password": "wrongpass"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == 429
    assert "Trop de tentatives" in response.text


def test_logout_symbolique(client):
    email = "logout@mail.com"
    creer_utilisateur(client, "logout", email, "bye123")

    login = client.post("/auth/token", data={
        "username": email,
        "password": "bye123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.post("/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Déconnecté avec succès"


def test_token_expiration(client):
    email = "expire@mail.com"
    creer_utilisateur(client, "expireuser", email, "exp123")

    token = create_access_token(
        data={"sub": email},
        expires_delta=1  # 1 minute
    )

    decoded = jwt.decode(token, key='', options={"verify_signature": False})
    exp = decoded.get("exp")
    print("Token expire à :", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp)))
    print("Heure actuelle :", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    print("Attente de l’expiration...")
    time.sleep(65)

    resp = client.get("/utilisateurs/moi", headers={
        "Authorization": f"Bearer {token}"
    })

    print("Statut après expiration:", resp.status_code, resp.text)
    assert resp.status_code == 401 or resp.status_code == 403
