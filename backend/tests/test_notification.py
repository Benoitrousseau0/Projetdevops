# backend/tests/test_notification.py

from fastapi.testclient import TestClient
# pytest -s tests/test_notification.py

def test_notification_apres_assignation(client: TestClient):
    # Créer employé, technicien, admin
    client.post("/utilisateurs/", json={
        "nom": "notifuser",
        "email": "notif@mail.com",
        "mot_de_passe": "notif123",
        "role": "employe"
    })
    client.post("/utilisateurs/", json={
        "nom": "tech",
        "email": "technotif@mail.com",
        "mot_de_passe": "tech123",
        "role": "technicien"
    })
    client.post("/utilisateurs/", json={
        "nom": "admin",
        "email": "adminnotif@mail.com",
        "mot_de_passe": "admin123",
        "role": "admin"
    })

    # Récupérer tokens
    emp_token = client.post("/auth/token", data={
        "username": "notif@mail.com",
        "password": "notif123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()["access_token"]

    admin_token = client.post("/auth/token", data={
        "username": "adminnotif@mail.com",
        "password": "admin123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()["access_token"]

    # Employé crée un ticket
    ticket = client.post("/tickets/", headers={
        "Authorization": f"Bearer {emp_token}"
    }, json={
        "titre": "Ticket notif",
        "description": "Besoin d'une notif",
        "priorite": "Faible"
    }).json()

    # Admin assigne le ticket au technicien (id=2 ici)
    assign = client.post(f"/tickets/{ticket['id']}/assigner", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=[2])
    print("Assignation:", assign.status_code, assign.text)
    assert assign.status_code == 200

    # Technicien se connecte et consulte ses notifications
    tech_token = client.post("/auth/token", data={
        "username": "technotif@mail.com",
        "password": "tech123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()["access_token"]

    resp = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech_token}"
    })
    print("Notifications:", resp.status_code, resp.text)
    assert resp.status_code == 200
    notifs = resp.json()
    assert any("assigné" in n["message"].lower() for n in notifs)


def test_marquer_lu(client: TestClient):
    # Créer employé, technicien, admin
    client.post("/utilisateurs/", json={
        "nom": "readuser",
        "email": "read@mail.com",
        "mot_de_passe": "read123",
        "role": "employe"
    })
    client.post("/utilisateurs/", json={
        "nom": "readtech",
        "email": "techread@mail.com",
        "mot_de_passe": "readtech123",
        "role": "technicien"
    })
    client.post("/utilisateurs/", json={
        "nom": "readadmin",
        "email": "adminread@mail.com",
        "mot_de_passe": "readadmin123",
        "role": "admin"
    })

    # Tokens
    emp_token = client.post("/auth/token", data={
        "username": "read@mail.com",
        "password": "read123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()["access_token"]

    admin_token = client.post("/auth/token", data={
        "username": "adminread@mail.com",
        "password": "readadmin123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()["access_token"]

    # Employé crée un ticket
    ticket = client.post("/tickets/", headers={
        "Authorization": f"Bearer {emp_token}"
    }, json={
        "titre": "Test read notif",
        "description": "notification test",
        "priorite": "Moyenne"
    }).json()

    # Admin assigne ticket au technicien (id=2 ici aussi)
    client.post(f"/tickets/{ticket['id']}/assigner", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=[2])

    # Technicien se connecte
    tech_resp = client.post("/auth/token", data={
        "username": "techread@mail.com",
        "password": "readtech123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert tech_resp.status_code == 200
    tech_token = tech_resp.json()["access_token"]

    # Récupérer ses notifications
    notif_list = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech_token}"
    }).json()

    assert len(notif_list) > 0
    notif_id = notif_list[0]["id"]

    # Marquer comme lue
    mark = client.post(f"/notifications/{notif_id}/lu", headers={
        "Authorization": f"Bearer {tech_token}"
    })
    print("Mark read:", mark.status_code, mark.text)
    assert mark.status_code == 200
    assert mark.json()["lu"] is True
