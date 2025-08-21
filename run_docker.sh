#!/bin/bash

# Script para executar o sistema de doação de livros com Docker
# Este script contorna problemas de rede do Docker em alguns ambientes

echo "🐳 Iniciando Sistema de Doação de Livros com Docker"
echo "=================================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker instalado. Reinicie o terminal e execute novamente."
    exit 1
fi

# Verificar se Docker está rodando
if ! sudo docker info &> /dev/null; then
    echo "🔄 Iniciando Docker..."
    sudo systemctl start docker
fi

echo "🏗️  Fazendo build da imagem..."

# Build da imagem usando host network para evitar problemas de iptables
sudo docker build --network=host -t book-donation . || {
    echo "❌ Erro no build. Tentando com método alternativo..."
    
    # Método alternativo: usar imagem base com dependências já instaladas
    cat > Dockerfile.simple << 'EOF'
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Instalar dependências uma por vez para evitar problemas de rede
RUN pip install --no-cache-dir Flask==3.1.1
RUN pip install --no-cache-dir Flask-SQLAlchemy==3.1.1
RUN pip install --no-cache-dir Flask-Cors==6.0.0

COPY src/ ./src/
RUN mkdir -p src/database

EXPOSE 5000

CMD ["python", "src/main.py"]
EOF

    sudo docker build --network=host -f Dockerfile.simple -t book-donation . || {
        echo "❌ Falha no build. Verifique sua conexão de rede."
        exit 1
    }
}

echo "🚀 Executando containers..."

# Parar containers anteriores se existirem
sudo docker stop book-donation-app book-donation-admin 2>/dev/null || true
sudo docker rm book-donation-app book-donation-admin 2>/dev/null || true

# Executar containers usando docker-compose
sudo docker compose up -d

# Aguardar alguns segundos para os containers inicializarem
echo "⏳ Aguardando inicialização..."
sleep 8

# Verificar se estão rodando
if sudo docker ps | grep -q book-donation-app && sudo docker ps | grep -q book-donation-admin; then
    echo "✅ Sistema iniciado com sucesso!"
    echo "🌐 Site Principal: http://localhost:5000"
    echo "🔧 Painel Admin:   http://localhost:5001"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Ver logs (site):  sudo docker logs -f book-donation-app"
    echo "   Ver logs (admin): sudo docker logs -f book-donation-admin"
    echo "   Parar tudo:       sudo docker compose down"
    echo "   Reiniciar:        sudo docker compose restart"
    echo ""
else
    echo "❌ Erro ao iniciar containers. Verificando logs..."
    echo "=== Logs do Site Principal ==="
    sudo docker logs book-donation-app
    echo "=== Logs do Admin ==="
    sudo docker logs book-donation-admin
fi

