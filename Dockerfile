FROM python:3.12-slim

# Configuration environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app

# Installation dépendances système (nécessaires pour certains calculs ou outils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Installation dépendances Python
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY backend/ /app/

# Exposition du port
EXPOSE 8000

# Commande de lancement (Gunicorn pour la prod, peut être surchargée pour le dev)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
