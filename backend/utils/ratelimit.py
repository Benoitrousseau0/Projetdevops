from collections import defaultdict
from datetime import datetime, timedelta

# Stocke les tentatives en mémoire (redis serait + solide en prod)
tentatives = defaultdict(list)
MAX_TENTATIVES = 5
FENETRE = timedelta(minutes=1)

def tentative_autorisee(email: str):
    maintenant = datetime.utcnow()
    tentatives[email] = [t for t in tentatives[email] if maintenant - t < FENETRE]
    return len(tentatives[email]) < MAX_TENTATIVES

def enregistrer_tentative(email: str):
    tentatives[email].append(datetime.utcnow())
