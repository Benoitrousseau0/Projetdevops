# Projetdevops


fastapi+react 
lancez: 
```
git clone "https://github.com/Benoitrousseau0/Projetdevops.git"
```
activez l'environnement backend, executez les commandes dans l'odre dans un terminal:
```
cd projetdevops
python -m venv .venv
cd .venv/scripts
./activate
cd ../..
pip install requirements.txt
```

lancez fastapi:
```
cd projetdevops/backend
uvicorn core.main:app --reload
```

lancez react (non fonctionnel pour le moment):
```
cd frontend
npm install # une seule fois lors du telechargement du projet
npm start
```
