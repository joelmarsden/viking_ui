from flask import Flask
from src.routes import main_bp
import logging


class SkipGET(logging.Filter):
    def filter(self, record):
        return 'GET ' not in record.getMessage()


logging.getLogger("werkzeug").addFilter(SkipGET())

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=9876)