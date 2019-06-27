from apps import app
from flask_cors import CORS

from views import user_app
from views.free_course_view import free_blue
from views.mine_view import mine_blue

APP_CONFIG={
    'host': 'localhost',
    'port': 8004,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(user_app.blue)
    app.register_blueprint(mine_blue)
    app.register_blueprint(free_blue)
    app.run(**APP_CONFIG)