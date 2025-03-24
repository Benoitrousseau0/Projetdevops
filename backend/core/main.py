from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routes import auth, utilisateur, ticket, commentaire, notification, test

# Création des tables à partir des modèles
Base.metadata.create_all(bind=engine)


# --------- test app: pytest -----------
# ---------  DEMARRAGE APP:   uvicorn core.main:app --reload ---------
# ou uvicorn core.main:app --port 8001
app = FastAPI(title="projet devops ticket")

# Autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à adapter selon ton environnement (localhost:3000 par exemple)
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

