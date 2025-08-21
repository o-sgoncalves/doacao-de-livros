# Biblioteca Solidária

Sistema web para doação de livros de tecnologia desenvolvido com Flask e Docker.

## Sobre o Projeto

A Biblioteca Solidária é uma plataforma que permite compartilhar livros de tecnologia com a comunidade. Os usuários podem visualizar livros disponíveis, fazer reservas e o administrador recebe notificações automáticas via Telegram para coordenar as entregas.

### Funcionalidades

- **Site Principal**: Catálogo de livros com sistema de reservas
- **Painel Administrativo**: Gerenciamento de livros e reservas
- **Notificações Telegram**: Alertas automáticos para novas reservas
- **Interface Responsiva**: Design moderno adaptado para todos os dispositivos
- **Dockerizado**: Deploy simples com Docker Compose

## Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask, SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Containerização**: Docker, Docker Compose
- **Integração**: Telegram Bot API
- **Proxy**: Cloudflare Tunnel (opcional)

## Estrutura do Projeto

```
├── src/
│   ├── models/          # Modelos do banco de dados
│   ├── routes/          # Rotas da API
│   ├── static/          # Arquivos estáticos (HTML, CSS, JS, imagens)
│   ├── database/        # Banco de dados SQLite
│   ├── main.py          # Aplicação principal
│   └── admin_app.py     # Painel administrativo
├── docker-compose.yml   # Configuração dos containers
├── Dockerfile          # Imagem Docker
├── requirements.txt    # Dependências Python
└── .env.example        # Exemplo de variáveis de ambiente
```

## Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose instalados
- Bot do Telegram configurado (opcional)

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/biblioteca-solidaria.git
cd biblioteca-solidaria
```

### 2. Configure as Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
TELEGRAM_BOT_TOKEN=seu_token_do_bot_telegram
TELEGRAM_CHAT_ID=seu_chat_id_telegram
```

### 3. Execute a Aplicação

```bash
docker compose up --build
```

### 4. Acesse a Aplicação

- **Site Principal**: http://localhost:5000
- **Painel Admin**: http://localhost:5001

## Configuração do Telegram Bot

### Criando o Bot

1. Converse com [@BotFather](https://t.me/BotFather) no Telegram
2. Digite `/newbot` e siga as instruções
3. Salve o token fornecido

### Obtendo o Chat ID

1. Envie uma mensagem para seu bot
2. Acesse: `https://api.telegram.org/botSEU_TOKEN/getUpdates`
3. Procure o valor em `"chat":{"id":123456789}`

## Deploy com Cloudflare Tunnel

Para expor a aplicação publicamente:

1. Configure um tunnel no [Cloudflare Zero Trust](https://dash.teams.cloudflare.com/)
2. Adicione o token no `docker-compose.yml`
3. Configure os subdominios apontando para:
   - Site principal: `http://book-donation-app:5000`
   - Painel admin: `http://book-donation-admin:5001`

## Uso da Aplicação

### Para Usuários

1. Acesse o site principal
2. Navegue pelos livros disponíveis
3. Clique em "Reservar" nos livros desejados
4. Preencha o formulário com seus dados
5. Confirme a reserva

### Para Administradores

1. Acesse o painel admin
2. **Aba Reservas**: Visualize e gerencie reservas ativas
3. **Aba Cadastrar**: Adicione novos livros usando URLs de imagem
4. Receba notificações automáticas no Telegram

## Desenvolvimento

### Estrutura do Banco de Dados

#### Tabela: books
- `id`: Identificador único
- `title`: Título do livro
- `author`: Autor
- `description`: Descrição
- `image`: URL da imagem
- `available`: Disponibilidade (boolean)
- `created_at`: Data de criação

#### Tabela: reservations
- `id`: Identificador único
- `name`: Nome do solicitante
- `email`: Email
- `address`: Endereço completo
- `phone`: Telefone
- `book_ids`: IDs dos livros (JSON)
- `status`: Status da reserva
- `created_at`: Data da reserva

### API Endpoints

#### Livros
- `GET /api/books` - Listar todos os livros
- `POST /api/books` - Criar novo livro
- `PUT /api/books/<id>` - Atualizar livro

#### Reservas
- `GET /api/reservations` - Listar reservas
- `POST /api/reservations` - Criar reserva
- `DELETE /api/reservations/<id>` - Cancelar reserva

### Executando em Desenvolvimento

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação principal
python src/main.py

# Executar painel admin (em outro terminal)
python src/admin_app.py
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Segurança

- Nunca commite credenciais no código
- Use variáveis de ambiente para dados sensíveis
- Configure GitHub Secrets para deploy automatizado
- Mantenha dependências atualizadas

## Troubleshooting

### Container não inicia
- Verifique se as portas 5000 e 5001 estão livres
- Confirme se o Docker está rodando
- Verifique logs: `docker logs book-donation-app`

### Notificações não chegam
- Confirme o token do bot no arquivo `.env`
- Verifique se o chat ID está correto
- Teste o bot enviando `/start`

### Banco de dados não persiste
- Verifique se o volume `book_data` está configurado
- Confirme permissões de escrita no diretório

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

**Samuel Gonçalves**
- LinkedIn: [linkedin.com/in/samuelgoncalvespereira](https://linkedin.com/in/samuelgoncalvespereira)
- Portfolio: [sgoncalves.tec.br](https://sgoncalves.tec.br)

---

Feito com dedicação para a comunidade tech 🚀