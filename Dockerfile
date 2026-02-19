# 1. Base: Python slim é leve
FROM python:3.11-slim

# 2. Configurações de ambiente para evitar logs "atrasados"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instala dependências do sistema para o banco de dados
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Define o diretório de trabalho
WORKDIR /app

# 5. Instala as bibliotecas do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o projeto para dentro do container
COPY . .