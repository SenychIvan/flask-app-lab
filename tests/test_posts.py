import pytest
from app import create_app, db
from app.posts.models import Post

@pytest.fixture
def app():
    app = create_app("testing")
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    """Тестуємо доступність сторінки постів"""
    response = client.get("/post/")
    assert response.status_code in (200, 302)


def test_create_post(app):
    """Тестуємо створення нового поста"""
    with app.app_context():
        post = Post(title="Test Post", content="Some content", category="news", author="Tester")
        db.session.add(post)
        db.session.commit()
        assert Post.query.count() == 1


def test_add_post_via_route(client):
    """Тестуємо додавання поста через форму (route)"""
    response = client.post("/post/create", data={
        "title": "Flask Test Post",
        "content": "Test content",
        "category": "tech",
        "is_active": "y",
    }, follow_redirects=True)
    assert response.status_code == 200
