from .extensions import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.text}>"
    
    def to_dict(self):
        """Convert message to dictionary for JSON responses"""
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

