from datetime import datetime
from enum import Enum
from app import db

# Enum для категорій
class CategoryEnum(Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"

# Модель Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.Enum(CategoryEnum), default=CategoryEnum.other)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        return f"<Post {self.id}: {self.title[:20]}>"
