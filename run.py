import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use Heroku's provided PORT environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))

    # Run the Flask app on 0.0.0.0 to bind to all available network interfaces
    app.run(host='0.0.0.0', port=port)
