import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from core.config import settings

# ça permet d'attendre que mysql marche
RETRIES = 10
WAIT = 3  # 3sec

for i in range(RETRIES):
    try:
        engine = create_engine(settings.DATABASE_URL)
        # on teste la connexion directe
        connection = engine.connect()
        connection.close()
        print("✅ Connected to MySQL database.")
        break
    except OperationalError:
        print(f"⏳ MySQL not ready (try {i + 1}/{RETRIES})... waiting {WAIT}s")
        time.sleep(WAIT)
else:
    print("❌ Could not connect to MySQL after several retries. Exiting.")
    exit(1)

# Session et base une fois la connexion OK
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
