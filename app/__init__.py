from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Ініціалізуємо ORM
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

from app.posts.models import Post


def create_app(config_name="development"):
    app = Flask(__name__)

    # Обираємо конфігурацію
    if config_name == "production":
        app.config.from_object(ProductionConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)

    # Реєстрація blueprint'ів
    from app.views import main
    app.register_blueprint(main)

    from app.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from app.products.views import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    from app.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix="/post")

    # Обробка помилки 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
