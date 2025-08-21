from flask import Blueprint, request, jsonify
from src.models.book import db, Book, Reservation
import json
import requests
import os
from datetime import datetime

book_bp = Blueprint('book', __name__)

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'SEU_TOKEN_AQUI')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'SEU_CHAT_ID_AQUI')

def send_telegram_notification(reservation_data):
    """Envia notificação para o Telegram quando uma reserva é feita"""
    try:
        # Formatar lista de livros
        books_list = "\n".join([
            f"📘 {book['title']} - {book['author']}" 
            for book in reservation_data['selected_books']
        ])
        
        # Montar mensagem
        message = f"""
🔔 NOVA RESERVA DE LIVROS!

👤 DADOS DO SOLICITANTE:
• Nome: {reservation_data['name']}
• Email: {reservation_data['email']}
• Telefone: {reservation_data['phone']}

📍 ENDEREÇO:
{reservation_data['address']}

📚 LIVROS RESERVADOS:
{books_list}

🆔 ID da Reserva: #{reservation_data['id']}
⏰ Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

💬 Entre em contato para combinar o envio!
        """.strip()
        
        # Enviar para o Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Notificação enviada para o Telegram com sucesso!")
            return True
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar notificação para Telegram: {str(e)}")
        return False

@book_bp.route('/books', methods=['GET'])
def get_books():
    """Retorna todos os livros disponíveis"""
    try:
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books', methods=['POST'])
def create_book():
    """Cria um novo livro"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['title', 'author', 'description', 'image']):
            return jsonify({'error': 'Campos obrigatórios: title, author, description, image'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            description=data['description'],
            image=data['image'],
            available=data.get('available', True)
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify(book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Atualiza um livro"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'description' in data:
            book.description = data['description']
        if 'image' in data:
            book.image = data['image']
        if 'available' in data:
            book.available = data['available']
        
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/reservations', methods=['POST'])
def create_reservation():
    """Cria uma nova reserva e envia notificação"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'address', 'phone', 'selectedBooks']
        if not all(key in data for key in required_fields):
            return jsonify({'error': f'Campos obrigatórios: {", ".join(required_fields)}'}), 400
        
        # Validar se os livros existem e estão disponíveis
        book_ids = [book['id'] for book in data['selectedBooks']]
        books = Book.query.filter(Book.id.in_(book_ids)).all()
        
        if len(books) != len(book_ids):
            return jsonify({'error': 'Alguns livros não foram encontrados'}), 400
        
        unavailable_books = [book for book in books if not book.available]
        if unavailable_books:
            return jsonify({'error': 'Alguns livros não estão mais disponíveis'}), 400
        
        # Criar a reserva
        reservation = Reservation(
            name=data['name'],
            email=data['email'],
            address=data['address'],
            phone=data['phone'],
            book_ids=json.dumps(book_ids)
        )
        
        db.session.add(reservation)
        
        # Marcar livros como indisponíveis
        for book in books:
            book.available = False
        
        db.session.commit()
        
        # Preparar dados para notificação e enviar
        reservation_dict = reservation.to_dict()
        send_telegram_notification(reservation_dict)
        
        return jsonify(reservation_dict), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/reservations', methods=['GET'])
def get_reservations():
    """Retorna todas as reservas"""
    try:
        reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
        return jsonify([reservation.to_dict() for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_bp.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    """Atualiza o status de uma reserva"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        data = request.get_json()
        
        if 'status' in data:
            reservation.status = data['status']
        
        db.session.commit()
        return jsonify(reservation.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500