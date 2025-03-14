from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Run the Flask application
if __name__ == '__main__':
    from app import app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5001)),
        debug=os.getenv('FLASK_DEBUG', '1') == '1'
    ) 