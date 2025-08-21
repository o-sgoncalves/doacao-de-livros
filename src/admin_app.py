import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from src.models.book import db, Book, Reservation
import json

# Criar aplicação Flask para administração
admin_app = Flask(__name__, static_folder='static', static_url_path='')

# Configuração do banco de dados
admin_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
admin_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(admin_app)
CORS(admin_app)

# Template HTML para o painel administrativo
ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo - Doação de Livros</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6B46C1 0%, #3B82F6 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .admin-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .admin-header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .admin-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        .tab-button {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .tab-button.active {
            background: white;
            color: #6B46C1;
        }
        
        .tab-button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .tab-content {
            display: none;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .section-header {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            padding: 20px;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .content-area {
            padding: 30px;
        }
        
        /* Estilos para reservas */
        .reservation-item {
            border-bottom: 1px solid #E5E7EB;
            padding: 20px 0;
            position: relative;
        }
        
        .reservation-item:last-child {
            border-bottom: none;
        }
        
        .reservation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .reservation-id {
            font-weight: bold;
            color: #6B46C1;
            font-size: 1.1em;
        }
        
        .cancel-btn {
            background: #DC2626;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        
        .cancel-btn:hover {
            background: #B91C1C;
        }
        
        .reservation-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .detail-group {
            background: #F3F4F6;
            padding: 15px;
            border-radius: 10px;
        }
        
        .detail-label {
            font-weight: bold;
            color: #374151;
            margin-bottom: 5px;
        }
        
        .detail-value {
            color: #6B7280;
            word-break: break-word;
        }
        
        .books-list {
            background: #EEF2FF;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #6B46C1;
        }
        
        .book-item {
            background: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #10B981;
        }
        
        /* Estilos para formulário de livros */
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            font-weight: bold;
            color: #374151;
            margin-bottom: 8px;
        }
        
        .form-input, .form-textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }
        
        .form-input:focus, .form-textarea:focus {
            outline: none;
            border-color: #6B46C1;
        }
        
        .form-textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #6B46C1 0%, #3B82F6 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(107, 70, 193, 0.4);
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        }
        
        .no-data {
            text-align: center;
            padding: 60px 20px;
            color: #6B7280;
            font-size: 1.1em;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #6B7280;
        }
        
        .error, .success {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .error {
            background: #FEE2E2;
            color: #DC2626;
            border-left: 4px solid #DC2626;
        }
        
        .success {
            background: #D1FAE5;
            color: #059669;
            border-left: 4px solid #059669;
        }
        
        @media (max-width: 768px) {
            .admin-tabs {
                flex-direction: column;
            }
            
            .reservation-details {
                grid-template-columns: 1fr;
            }
            
            .reservation-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>🔧 Painel Administrativo</h1>
            <p>Gerencie reservas e cadastre novos livros</p>
            <p><strong>Porta Admin:</strong> 5001 | <strong>Site Principal:</strong> 5000</p>
        </div>
        
        <div class="admin-tabs">
            <button class="tab-button active" onclick="showTab('reservations')">📋 Reservas</button>
            <button class="tab-button" onclick="showTab('books')">📚 Cadastrar Livros</button>
        </div>
        
        <!-- Tab de Reservas -->
        <div id="reservations-tab" class="tab-content active">
            <div class="section-header">
                📋 Gerenciar Reservas
            </div>
            <div class="content-area">
                <button class="refresh-btn" onclick="loadReservations()">
                    🔄 Atualizar Reservas
                </button>
                <div id="reservations-content">
                    <div class="loading">Carregando reservas...</div>
                </div>
            </div>
        </div>
        
        <!-- Tab de Cadastro de Livros -->
        <div id="books-tab" class="tab-content">
            <div class="section-header">
                📚 Cadastrar Novo Livro
            </div>
            <div class="content-area">
                <div id="book-message"></div>
                <form id="book-form">
                    <div class="form-group">
                        <label class="form-label" for="title">Título do Livro *</label>
                        <input type="text" id="title" class="form-input" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="author">Autor *</label>
                        <input type="text" id="author" class="form-input" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="description">Descrição *</label>
                        <textarea id="description" class="form-textarea" required placeholder="Ex: 3ª Edição - Aprenda a criar aplicações..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="image">Nome da Imagem *</label>
                        <input type="text" id="image" class="form-input" required placeholder="Ex: 20250821_114534.jpg">
                        <small style="color: #6B7280; margin-top: 5px; display: block;">
                            Coloque a imagem na pasta /src/static/images/ e digite apenas o nome do arquivo
                        </small>
                    </div>
                    
                    <button type="submit" class="submit-btn">
                        ➕ Cadastrar Livro
                    </button>
                </form>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="http://localhost:5000" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                🌐 Abrir Site Principal (Porta 5000)
            </a>
        </div>
    </div>

    <script>
        // Função para alternar entre abas
        function showTab(tabName) {
            // Esconder todas as abas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remover classe active de todos os botões
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Mostrar aba selecionada
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // Ativar botão correspondente
            event.target.classList.add('active');
            
            // Carregar dados se necessário
            if (tabName === 'reservations') {
                loadReservations();
            }
        }
        
        // Função para carregar reservas
        async function loadReservations() {
            const content = document.getElementById('reservations-content');
            content.innerHTML = '<div class="loading">Carregando reservas...</div>';
            
            try {
                const response = await fetch('/api/reservations');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const reservations = await response.json();
                
                if (reservations.length === 0) {
                    content.innerHTML = `
                        <div class="no-data">
                            📚 Nenhuma reserva encontrada ainda.<br>
                            Quando alguém reservar livros, aparecerão aqui!
                        </div>
                    `;
                    return;
                }
                
                content.innerHTML = reservations.map(reservation => `
                    <div class="reservation-item">
                        <div class="reservation-header">
                            <div class="reservation-id">Reserva #${reservation.id}</div>
                            <div>
                                <span style="color: #6B7280; margin-right: 15px;">${formatDate(reservation.created_at)}</span>
                                <button class="cancel-btn" onclick="cancelReservation(${reservation.id})">
                                    ❌ Cancelar Reserva
                                </button>
                            </div>
                        </div>
                        
                        <div class="reservation-details">
                            <div class="detail-group">
                                <div class="detail-label">👤 Nome:</div>
                                <div class="detail-value">${reservation.name}</div>
                            </div>
                            
                            <div class="detail-group">
                                <div class="detail-label">📧 Email:</div>
                                <div class="detail-value">${reservation.email}</div>
                            </div>
                            
                            <div class="detail-group">
                                <div class="detail-label">📞 Telefone:</div>
                                <div class="detail-value">${reservation.phone}</div>
                            </div>
                            
                            <div class="detail-group">
                                <div class="detail-label">📍 Endereço:</div>
                                <div class="detail-value">${reservation.address.replace(/\\n/g, '<br>')}</div>
                            </div>
                        </div>
                        
                        <div class="books-list">
                            <div style="font-weight: bold; color: #6B46C1; margin-bottom: 10px;">📚 Livros Reservados:</div>
                            ${reservation.selected_books.map(book => `
                                <div class="book-item">
                                    <strong>${book.title}</strong> - ${book.author}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('');
                
            } catch (error) {
                console.error('Erro ao carregar reservas:', error);
                content.innerHTML = `
                    <div class="error">
                        ❌ Erro ao carregar reservas: ${error.message}<br>
                        Verifique se o servidor está funcionando e tente novamente.
                    </div>
                `;
            }
        }
        
        // Função para cancelar reserva
        async function cancelReservation(reservationId) {
            if (!confirm('Tem certeza que deseja cancelar esta reserva? Os livros ficarão disponíveis novamente.')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/reservations/${reservationId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                alert('Reserva cancelada com sucesso! Os livros estão disponíveis novamente.');
                loadReservations(); // Recarregar lista
                
            } catch (error) {
                console.error('Erro ao cancelar reserva:', error);
                alert('Erro ao cancelar reserva: ' + error.message);
            }
        }
        
        // Função para cadastrar livro
        document.getElementById('book-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const messageDiv = document.getElementById('book-message');
            const submitBtn = e.target.querySelector('.submit-btn');
            
            // Desabilitar botão durante envio
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Cadastrando...';
            
            const formData = {
                title: document.getElementById('title').value,
                author: document.getElementById('author').value,
                description: document.getElementById('description').value,
                image: 'images/' + document.getElementById('image').value
            };
            
            try {
                const response = await fetch('/api/books', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erro desconhecido');
                }
                
                const result = await response.json();
                
                messageDiv.innerHTML = `
                    <div class="success">
                        ✅ Livro "${result.title}" cadastrado com sucesso!
                    </div>
                `;
                
                // Limpar formulário
                document.getElementById('book-form').reset();
                
            } catch (error) {
                console.error('Erro ao cadastrar livro:', error);
                messageDiv.innerHTML = `
                    <div class="error">
                        ❌ Erro ao cadastrar livro: ${error.message}
                    </div>
                `;
            } finally {
                // Reabilitar botão
                submitBtn.disabled = false;
                submitBtn.textContent = '➕ Cadastrar Livro';
            }
        });
        
        // Função para formatar data
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('pt-BR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        // Carregar reservas quando a página carregar
        document.addEventListener('DOMContentLoaded', loadReservations);
        
        // Atualizar automaticamente a cada 30 segundos
        setInterval(loadReservations, 30000);
    </script>
</body>
</html>
'''

@admin_app.route('/')
def admin_panel():
    """Página principal do painel administrativo"""
    return render_template_string(ADMIN_TEMPLATE)

@admin_app.route('/api/reservations', methods=['GET'])
def get_reservations():
    """Listar todas as reservas"""
    try:
        reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
        return jsonify([reservation.to_dict() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_app.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    """Cancelar uma reserva e tornar os livros disponíveis novamente"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # Buscar os livros da reserva e torná-los disponíveis
        book_ids = json.loads(reservation.book_ids)
        books = Book.query.filter(Book.id.in_(book_ids)).all()
        
        for book in books:
            book.available = True
        
        # Remover a reserva
        db.session.delete(reservation)
        db.session.commit()
        
        return jsonify({'message': 'Reserva cancelada com sucesso', 'books_freed': len(books)}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_app.route('/api/books', methods=['POST'])
def create_book():
    """Cadastrar um novo livro"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['title', 'author', 'description', 'image']):
            return jsonify({'error': 'Campos obrigatórios: title, author, description, image'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            description=data['description'],
            image=data['image'],
            available=True
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify(book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with admin_app.app_context():
        db.create_all()
    admin_app.run(host='0.0.0.0', port=5001, debug=True)

