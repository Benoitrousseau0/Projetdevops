# tests/test_utilisateur.py
# pytest -s tests/test_utilisateur.py

import uuid

def email_unique(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@mail.com"

def creer_utilisateur_et_token(client, nom, email, mot_de_passe, role="employe"):
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    resp = client.post("/utilisateurs/", json={
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": role
    }, headers=headers)
    assert resp.status_code == 200

    login = client.post("/auth/token", data={
        "username": email,
        "password": mot_de_passe
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert login.status_code == 200

    return login.json()["access_token"]

def test_inscription_utilisateur(client):
    admin = client.post("/tests/create-admin").json()
    token = admin["token"]
    response = client.post("/utilisateurs/", json={
        "nom": "user1",
        "email": email_unique("user1"),
        "mot_de_passe": "userpass",
        "role": "employe"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "email" in response.json()

def test_email_deja_utilise(client):
    email = email_unique("user2")
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    client.post("/utilisateurs/", json={
        "nom": "user2",
        "email": email,
        "mot_de_passe": "pass123",
        "role": "employe"
    }, headers=headers)
    response = client.post("/utilisateurs/", json={
        "nom": "user2-bis",
        "email": email,
        "mot_de_passe": "pass123",
        "role": "employe"
    }, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email déjà utilisé"

def test_get_profil_connecte(client):
    email = email_unique("user3")
    token = creer_utilisateur_et_token(client, "user3", email, "testpass", "employe")

    response = client.get("/utilisateurs/moi", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()["email"] == email

def test_update_profil_utilisateur(client):
    email = email_unique("update")
    token = creer_utilisateur_et_token(client, "update", email, "up123456", "employe")
    new_email = email_unique("newmail")

    update = client.put("/utilisateurs/moi", json={
        "nom": "newname",
        "email": new_email
    }, headers={"Authorization": f"Bearer {token}"})

    assert update.status_code == 200
    assert update.json()["email"] == new_email
    assert update.json()["nom"] == "newname"

def test_modification_mot_de_passe(client):
    email = email_unique("passuser")
    token = creer_utilisateur_et_token(client, "passuser", email, "oldpass123", "employe")

    # Modifier le mot de passe
    resp = client.put("/utilisateurs/password", json={
        "ancien_mot_de_passe": "oldpass123",
        "nouveau_mot_de_passe": "newpassword"
    }, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    assert resp.status_code == 200
    assert resp.json()["message"] == "Mot de passe mis à jour"

    # Vérifie que l'ancien mot de passe échoue
    fail = client.post("/auth/token", data={
        "username": email,
        "password": "oldpass123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert fail.status_code == 401

    # Nouveau mot de passe fonctionne
    success = client.post("/auth/token", data={
        "username": email,
        "password": "newpassword"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert success.status_code == 200

def test_suppression_propre_compte(client):
    email = email_unique("del")
    token = creer_utilisateur_et_token(client, "deleteuser", email, "del12345", "employe")

    resp = client.delete("/utilisateurs/moi", headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    assert resp.json()["message"] == "Compte supprimé"

def test_suppression_autre_utilisateur_par_admin(client):
    email = email_unique("victime")
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    creation = client.post("/utilisateurs/", json={
        "nom": "victime_suppr",
        "email": email,
        "mot_de_passe": "victime123",
        "role": "employe"
    }, headers=headers)
    assert creation.status_code == 200
    user_id = creation.json()["id"]

    resp = client.delete(f"/utilisateurs/{user_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Utilisateur supprimé avec succès"

def test_employe_ne_peut_pas_lister_utilisateurs(client):
    email = email_unique("employe")
    token = creer_utilisateur_et_token(client, "Simple Employé", email, "employepass", "employe")

    response = client.get("/utilisateurs/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"
