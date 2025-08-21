# 🐳 Site de Doação de Livros - Versão Docker

Este projeto está completamente dockerizado para facilitar o deploy e execução em qualquer ambiente.

## 🚀 Como Executar com Docker

### Opção 1: Docker Compose (Recomendado)

```bash
# Clone ou extraia o projeto
cd book_donation_backend

# Execute com docker-compose
docker-compose up -d

# Acesse o site
open http://localhost:5000
```

### Opção 2: Docker Build Manual

```bash
# Build da imagem
docker build -t book-donation .

# Execute o container
docker run -d \
  --name book-donation-app \
  -p 5000:5000 \
  -v book_data:/app/src/database \
  book-donation

# Acesse o site
open http://localhost:5000
```

## 📋 Comandos Úteis

### Gerenciar Containers
```bash
# Ver logs
docker-compose logs -f

# Parar o serviço
docker-compose down

# Reiniciar
docker-compose restart

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose down -v
```

### Backup do Banco de Dados
```bash
# Fazer backup
docker cp book-donation-backend:/app/src/database/app.db ./backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar backup
docker cp backup_20250821_123456.db book-donation-backend:/app/src/database/app.db
docker-compose restart
```

### Monitoramento
```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats book-donation-backend

# Health check
docker inspect --format='{{.State.Health.Status}}' book-donation-backend
```

## 🔧 Configurações

### Variáveis de Ambiente
Edite o `docker-compose.yml` para personalizar:

```yaml
environment:
  - FLASK_ENV=production          # ou development
  - PYTHONUNBUFFERED=1
  - SECRET_KEY=sua_chave_secreta  # opcional
```

### Portas
Para usar uma porta diferente:

```yaml
ports:
  - "8080:5000"  # Acesse via http://localhost:8080
```

### Volumes Persistentes
O banco de dados é automaticamente persistido no volume `book_data`.

## 🏗 Estrutura Docker

```
book_donation_backend/
├── Dockerfile              # Imagem do backend
├── docker-compose.yml      # Orquestração
├── .dockerignore           # Arquivos ignorados
├── requirements.txt        # Dependências Python
└── src/                    # Código da aplicação
```

## 🔒 Segurança

### Produção
Para ambiente de produção, considere:

1. **Usar HTTPS**:
```yaml
environment:
  - FLASK_ENV=production
  - SSL_CERT=/path/to/cert.pem
  - SSL_KEY=/path/to/key.pem
```

2. **Proxy Reverso** (Nginx):
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

3. **Secrets**:
```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## 📊 Monitoramento

### Logs Estruturados
```bash
# Logs em tempo real
docker-compose logs -f book-donation-app

# Logs específicos
docker-compose logs --tail=100 book-donation-app
```

### Health Checks
O container inclui health checks automáticos:
- Intervalo: 30 segundos
- Timeout: 30 segundos
- Retries: 3 tentativas

## 🚀 Deploy em Produção

### Docker Swarm
```bash
# Inicializar swarm
docker swarm init

# Deploy
docker stack deploy -c docker-compose.yml book-donation
```

### Kubernetes
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: book-donation
spec:
  replicas: 2
  selector:
    matchLabels:
      app: book-donation
  template:
    metadata:
      labels:
        app: book-donation
    spec:
      containers:
      - name: book-donation
        image: book-donation:latest
        ports:
        - containerPort: 5000
```

## 🔧 Troubleshooting

### Container não inicia
```bash
# Ver logs de erro
docker-compose logs book-donation-app

# Verificar saúde
docker inspect book-donation-backend
```

### Banco de dados corrompido
```bash
# Remover volume e recriar
docker-compose down -v
docker-compose up -d
```

### Porta em uso
```bash
# Verificar processos na porta
lsof -i :5000

# Usar porta diferente
docker-compose up -d --scale book-donation-app=0
# Editar docker-compose.yml
docker-compose up -d
```

## 📈 Performance

### Otimizações
- Imagem multi-stage para reduzir tamanho
- Cache de dependências Python
- Health checks para disponibilidade
- Volumes persistentes para dados

### Recursos Recomendados
- **CPU**: 0.5 cores mínimo
- **RAM**: 512MB mínimo
- **Disco**: 1GB para aplicação + dados

## 🎯 Vantagens da Versão Docker

✅ **Portabilidade**: Roda em qualquer ambiente  
✅ **Isolamento**: Não interfere com o sistema host  
✅ **Escalabilidade**: Fácil de escalar horizontalmente  
✅ **Backup**: Volumes persistentes para dados  
✅ **Monitoramento**: Health checks integrados  
✅ **Deploy**: Um comando para subir tudo  

**Pronto para produção!** 🚀

