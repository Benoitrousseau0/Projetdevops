# tests/test_notification.py
# pytest -s tests/test_notification.py

from fastapi.testclient import TestClient
import uuid

def email_unique(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@mail.com"

def creer_utilisateur_et_token(client: TestClient, nom: str, email: str, mot_de_passe: str) -> str:
    # Créer l'utilisateur via un admin
    admin = client.post("/tests/create-admin").json()
    headers = {"Authorization": f"Bearer {admin['token']}"}

    resp = client.post("/utilisateurs/", json={
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "role": "employe"
    }, headers=headers)
    assert resp.status_code == 200

    # Login
    resp = client.post("/auth/token", data={
        "username": email,
        "password": mot_de_passe
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_notification_apres_assignation(client: TestClient):
    emp_email = email_unique("emp")
    emp_token = creer_utilisateur_et_token(client, "notifuser", emp_email, "notif123")

    # Admin & Technicien
    admin = client.post("/tests/create-admin").json()
    tech = client.post("/tests/create-technicien").json()

    ticket = client.post("/tickets/", headers={
        "Authorization": f"Bearer {emp_token}"
    }, json={
        "titre": "Ticket notif",
        "description": "Besoin d'une notif",
        "priorite": "faible"
    }).json()

    assign = client.post(f"/tickets/{ticket['id']}/assigner", headers={
        "Authorization": f"Bearer {admin['token']}"
    }, json=[tech["id"]])
    print("Assignation:", assign.status_code, assign.text)
    assert assign.status_code == 200

    notifs = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech['token']}"
    })
    print("Notifications:", notifs.status_code, notifs.text)
    assert notifs.status_code == 200
    data = notifs.json()
    assert any("assigné" in n["message"].lower() for n in data)

def test_marquer_lu(client: TestClient):
    emp_email = email_unique("emp")
    emp_token = creer_utilisateur_et_token(client, "readuser", emp_email, "r123456")

    admin = client.post("/tests/create-admin").json()
    tech = client.post("/tests/create-technicien").json()

    ticket = client.post("/tickets/", headers={
        "Authorization": f"Bearer {emp_token}"
    }, json={
        "titre": "Test read notif",
        "description": "notification test",
        "priorite": "moyenne"
    }).json()

    client.post(f"/tickets/{ticket['id']}/assigner", headers={
        "Authorization": f"Bearer {admin['token']}"
    }, json=[tech["id"]])

    notif_list = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech['token']}"
    }).json()

    assert len(notif_list) > 0
    notif_id = notif_list[0]["id"]

    mark = client.post(f"/notifications/{notif_id}/lu", headers={
        "Authorization": f"Bearer {tech['token']}"
    })
    print("Mark read:", mark.status_code, mark.text)
    assert mark.status_code == 200
    assert mark.json()["lu"] is True

def test_marquer_toutes_lues(client: TestClient):
    emp_email = email_unique("emp")
    emp_token = creer_utilisateur_et_token(client, "bulkuser", emp_email, "b123456")

    admin = client.post("/tests/create-admin").json()
    tech = client.post("/tests/create-technicien").json()

    for i in range(2):
        ticket = client.post("/tickets/", headers={
            "Authorization": f"Bearer {emp_token}"
        }, json={
            "titre": f"Ticket {i}",
            "description": "Test bulk",
            "priorite": "moyenne"
        }).json()

        client.post(f"/tickets/{ticket['id']}/assigner", headers={
            "Authorization": f"Bearer {admin['token']}"
        }, json=[tech["id"]])

    notifs = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech['token']}"
    }).json()
    assert len(notifs) >= 2
    assert any(not n["lu"] for n in notifs)

    resp = client.post("/notifications/lu-toutes", headers={
        "Authorization": f"Bearer {tech['token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["message"] == "Toutes les notifications ont été marquées comme lues"

    notifs_apres = client.get("/notifications/", headers={
        "Authorization": f"Bearer {tech['token']}"
    }).json()
    assert all(n["lu"] for n in notifs_apres)
