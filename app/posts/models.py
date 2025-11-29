from datetime import datetime
from .. import db

# ============================================================

# ============================================================
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
)

# ============================================================

# ============================================================
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-many: Tags ↔ Posts
    posts = db.relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


# ============================================================
# ============================================================
class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    # One-to-many: Foreign Key на users.id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Зв’язок із User
    user = db.relationship("User", back_populates="posts")

    # Many-to-many: Posts ↔ Tags
    tags = db.relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.title[:20]}>"
