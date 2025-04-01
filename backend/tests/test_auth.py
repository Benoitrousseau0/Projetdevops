# backend/tests/test_auth.py
# pytest -s tests/test_auth.py

def test_login_succes(client):
    # Création de l'utilisateur
    response_creation = client.post("/utilisateurs/", json={
        "nom": "testuser",
        "email": "test@mail.com",
        "mot_de_passe": "secret",
        "role": "employe"
    })
    assert response_creation.status_code == 200, f"Erreur création utilisateur : {response_creation.text}"
    print("Réponse création:", response_creation.status_code, response_creation.json())

    # Tentative de login avec les bons identifiants
    response = client.post("/auth/token", data={
        "username": "test@mail.com",
        "password": "secret"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    print("Réponse login:", response.status_code, response.text)
    assert response.status_code == 200, f"Échec login : {response.text}"

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_login_echec(client):
    # Login avec mauvais mot de passe
    client.post("/utilisateurs/", json={
        "nom": "wrongpass",
        "email": "wrong@mail.com",
        "mot_de_passe": "abc123",
        "role": "Employe"
    })

    response = client.post("/auth/token", data={
        "username": "wrong@mail.com",
        "password": "incorrect"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"
