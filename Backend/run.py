from app import app
from app.config.config import DEBUG_MODE, APP_PORT
if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, port=APP_PORT, host='0.0.0.0')
