from flask import Flask, render_template
from api.cv_routes import cv_bp
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger()

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(cv_bp)

@app.route('/')
def index():
    logger.info("Accessing root endpoint")
    return render_template('home.html')

if __name__ == '__main__':
    logger.info("Starting Flask server")
    try:
        # init_db()
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start Flask server: {str(e)}")
        raise