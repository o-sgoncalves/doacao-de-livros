from src.models.user import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'image': self.image,
            'available': self.available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    book_ids = db.Column(db.Text, nullable=False)  # JSON string of book IDs
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        import json
        
        # Buscar informações dos livros
        book_ids = json.loads(self.book_ids) if self.book_ids else []
        books = Book.query.filter(Book.id.in_(book_ids)).all()
        selected_books = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
            'book_ids': book_ids,
            'selected_books': selected_books,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

