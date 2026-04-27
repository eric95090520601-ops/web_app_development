import os
from flask import Flask
from config import Config
from app.models import db
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.recipe import recipe_bp
from app.routes.comment import comment_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(Config)

    # 初始化資料庫
    db.init_app(app)

    # 註冊 Blueprints (路由)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(comment_bp)

    # 確保 instance 資料夾存在，並在首次啟動時建立資料表
    with app.app_context():
        os.makedirs(app.instance_path, exist_ok=True)
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
