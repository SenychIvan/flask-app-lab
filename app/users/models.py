from .. import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Додати зв’язок!
    posts = db.relationship("Post", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
