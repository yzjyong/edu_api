from apps import app
from flask_cors import CORS
<<<<<<< HEAD

from views import user_app
from views.free_course_view import free_blue
from views.mine_view import mine_blue
=======
from views import user_app,cart_app
>>>>>>> dc4c04619074005849b6a5137a082d1d21c67f18

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
    app.run(**APP_CONFIG)