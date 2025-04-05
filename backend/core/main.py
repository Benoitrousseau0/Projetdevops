from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routes import auth, utilisateur, ticket, commentaire, notification, test, test_util

# Création des tables à partir des modèles
Base.metadata.create_all(bind=engine)


# --------- test app: pytest -----------
# ---------  DEMARRAGE APP:   uvicorn core.main:app --reload ---------
# ou uvicorn core.main:app --port 8001
app = FastAPI(title="projet devops ticket")

# Autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(auth.router)
app.include_router(utilisateur.router)
app.include_router(ticket.router)
app.include_router(commentaire.router)
app.include_router(notification.router)
app.include_router(test.router)
app.include_router(test_util.router)

# bouton supp et modif commentaire
# techniciens supp, meilleur interface   VVVV
# plus d'options admin, dashboard info data ticket, voir +
# creation user par admin pas d'inscriptions solo
# fermé: on peut plus toucher, juste supp (seulement admin)