import logging
from flask import Flask
from flask_cors import CORS
from web.config import FLASK_PORT
from web.routes import api_bp

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=True)