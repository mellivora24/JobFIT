from flask import Flask
from api.cv_routes import cv_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(cv_bp)

@app.route('/')
def index():
    return "JobFIT API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)