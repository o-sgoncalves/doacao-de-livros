# Site de Doação de Livros de Tecnologia

Este é um site simples para facilitar a doação de livros de tecnologia. Os usuários podem visualizar os livros disponíveis, selecioná-los e fornecer seus dados de contato e endereço para recebimento.

## Características

- **Interface simples e responsiva**: Funciona bem em desktop e mobile
- **Seleção múltipla**: Permite selecionar vários livros de uma vez
- **Formulário completo**: Coleta nome, email, endereço completo e telefone
- **Aviso sobre frete**: Deixa claro que o custo do frete é por conta do interessado
- **Controle de disponibilidade**: Livros reservados ficam indisponíveis automaticamente

## Como usar

1. **Visualizar livros**: Os livros disponíveis são exibidos em cards com título, autor e descrição
2. **Selecionar livros**: Clique em "Selecionar" nos livros desejados
3. **Preencher formulário**: Complete todos os campos obrigatórios:
   - Nome completo
   - Email
   - Endereço completo (rua, número, complemento, bairro, cidade, estado, CEP)
   - Telefone com DDD
4. **Confirmar reserva**: Clique em "Confirmar Reserva" para finalizar

## Como personalizar

### Adicionar/Editar livros

Edite o arquivo `js/script.js` e modifique o array `books` no início do arquivo:

```javascript
const books = [
    {
        id: 1,
        title: "Nome do Livro",
        author: "Nome do Autor",
        description: "Descrição do livro",
        image: "URL_da_imagem_ou_placeholder",
        available: true
    },
    // Adicione mais livros aqui...
];
```

### Personalizar cores e estilo

Edite o arquivo `css/style.css` para alterar:
- Cores do cabeçalho (`.header`)
- Cores dos botões
- Layout dos cards
- Fontes e espaçamentos

## Hospedagem no GitHub Pages

### Passo 1: Criar repositório no GitHub
1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nomeie o repositório (ex: `book-donation-site`)
4. Marque como "Public"
5. Clique em "Create repository"

### Passo 2: Fazer upload dos arquivos
1. Na página do repositório, clique em "uploading an existing file"
2. Arraste todos os arquivos do projeto para a área de upload:
   - `index.html`
   - `css/style.css`
   - `js/script.js`
   - `README.md`
3. Adicione uma mensagem de commit (ex: "Adicionar site de doação de livros")
4. Clique em "Commit changes"

### Passo 3: Ativar GitHub Pages
1. No repositório, vá em "Settings"
2. Role para baixo até a seção "Pages"
3. Em "Source", selecione "Deploy from a branch"
4. Em "Branch", selecione "main" (ou "master")
5. Deixe a pasta como "/ (root)"
6. Clique em "Save"

### Passo 4: Acessar o site
- Aguarde alguns minutos
- O site estará disponível em: `https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO`
- O GitHub mostrará a URL na seção Pages

## Estrutura de arquivos

```
book_donation_site/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos CSS
├── js/
│   └── script.js       # Funcionalidades JavaScript
└── README.md           # Este arquivo
```

## Tecnologias utilizadas

- HTML5
- CSS3 (com Grid e Flexbox)
- JavaScript (ES6+)
- Design responsivo

## Funcionalidades implementadas

✅ Lista de livros com informações básicas  
✅ Seleção múltipla de livros  
✅ Formulário de reserva com validação  
✅ Controle de disponibilidade  
✅ Design responsivo  
✅ Aviso sobre custo do frete  
✅ Interface intuitiva e limpa  

## Próximos passos (opcionais)

Para uma versão mais avançada, você poderia adicionar:
- Backend para armazenar as reservas
- Sistema de autenticação
- Painel administrativo
- Integração com correios para cálculo de frete
- Sistema de notificações por email

## Suporte

Este é um projeto estático que funciona apenas no frontend. As reservas são simuladas (aparecem no console do navegador). Para um sistema completo de produção, seria necessário implementar um backend.

---

**Importante**: Lembre-se de personalizar a lista de livros no arquivo `js/script.js` com seus livros reais antes de publicar o site!

