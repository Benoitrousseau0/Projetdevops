FROM python:3.10-slim

WORKDIR /app

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# attente de mysql 
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

# Utilise wait-for-it pour attendre que MySQL soit prêt
CMD ["/wait-for-it.sh", "db:3306", "--", "uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
