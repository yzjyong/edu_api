from apps import app
from flask_cors import CORS
from views.free_course_view import free_blue
from views.mine_view import mine_blue
from views import user_app,cart_app,details_app


APP_CONFIG={
    'host': '0.0.0.0',
    'port': 8004,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(user_app.blue)
    app.register_blueprint(mine_blue)
    app.register_blueprint(free_blue)
    app.register_blueprint(cart_app.cart_blue)
    app.register_blueprint(details_app.blue)
    app.run(**APP_CONFIG)