from flask import Flask, Response
from flask_cors import CORS
from config.config import Config
from controllers.chat_controller import chat_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "supports_credentials": True,
            "methods": ["GET", "POST", "OPTIONS", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "X-SSE"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, port=Config.PORT)
