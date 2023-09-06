from flask import Flask
from routes.main import main_bp

# Create a Flask application
app = Flask(__name__)

# Register the main_bp Blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
