import os
from flask import Flask

def create_app(test_config=None):
    # 初始化 Flask application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key_for_flash'),
    )

    if test_config is None:
        # 當非測試模式時，載入 instance config 若存在
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在 (用來存放 SQLite DB)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊路由
    from .routes import register_routes
    register_routes(app)
    
    return app
