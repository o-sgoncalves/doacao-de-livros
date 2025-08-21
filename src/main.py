import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.book import Book
from src.routes.user import user_bp
from src.routes.book import book_bp
from src.routes.admin import admin_bp
import json

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(book_bp, url_prefix='/api')
app.register_blueprint(admin_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_books():
    """Inicializa os livros no banco de dados"""
    books_data = [
        {
            "title": "Programação Shell Linux",
            "author": "Julio Cezar Neves",
            "description": "10ª Edição - Atualizado com as novidades do Bash 4.0",
            "image": "images/20250821_114534.jpg"
        },
        {
            "title": "Google Android",
            "author": "Ricardo R. Lecheta",
            "description": "3ª Edição - Aprenda a criar aplicações para dispositivos móveis com o Android SDK",
            "image": "images/20250821_114551.jpg"
        },
        {
            "title": "Windows Server 2008 Guia Completo",
            "author": "William R. Stanek",
            "description": "Guia definitivo, centenas de soluções práticas",
            "image": "images/20250821_114612.jpg"
        },
        {
            "title": "Linux Network Administration",
            "author": "3Way Networks",
            "description": "Seja um profissional aprendendo com profissionais",
            "image": "images/20250821_114624.jpg"
        },
        {
            "title": "Linux Security Administration",
            "author": "3Way Networks",
            "description": "Seja um profissional aprendendo com profissionais",
            "image": "images/20250821_114634.jpg"
        },
        {
            "title": "Linux System Administration",
            "author": "3Way Networks",
            "description": "Seja um profissional aprendendo com profissionais",
            "image": "images/20250821_114647.jpg"
        },
        {
            "title": "Steve Jobs",
            "author": "Walter Isaacson",
            "description": "Biografia de Steve Jobs",
            "image": "images/20250821_114759.jpg"
        },
        {
            "title": "Jovem e Bem-Sucedido",
            "author": "Juliano Niederauer",
            "description": "Um guia para a realização profissional e financeira",
            "image": "images/20250821_114936.jpg"
        },
        {
            "title": "Educação Física: Ensino & Mudanças",
            "author": "Elenor Kunz",
            "description": "Coleção Educação Física",
            "image": "images/20250821_114942.jpg"
        }
    ]
    
    # Verificar se já existem livros no banco
    if Book.query.count() == 0:
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        db.session.commit()
        print("Livros inicializados no banco de dados!")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Se for a rota admin, não servir arquivo estático
    if path == 'admin':
        return admin_bp.admin_panel()
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_books()
    app.run(host='0.0.0.0', port=5001, debug=True)

