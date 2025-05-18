from flask import Flask
from dotenv import load_dotenv
from backend.routers.app_routers import init_routes

load_dotenv()

app = Flask(__name__)
init_routes(app)

if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        raise