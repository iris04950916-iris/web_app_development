from .auth import auth_bp
from .activity import activity_bp

def register_routes(app):
    """
    傳入 Flask 實例並註冊所有路由 Blueprint
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(activity_bp)
