from apigateway import app

from config import APP_HOST

if __name__ == '__main__':
    app.run(host=APP_HOST, port=5000)
