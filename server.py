from apps import app
from flask_cors import CORS
from views import user_app,cart_app

APP_CONFIG={
    'host': 'localhost',
    'port': 8004,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(user_app.blue)
    app.register_blueprint(cart_app.cart_blue)

    app.run(**APP_CONFIG)