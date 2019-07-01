from apps import app
from flask_cors import CORS

from views import user_app, cart_app, details_app, mine_app, free_course_app, combat_course_app,order_app



APP_CONFIG={
    'host': '0.0.0.0',
    'port': 8004,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(user_app.blue)
    app.register_blueprint(mine_app.mine_blue)
    app.register_blueprint(free_course_app.free_blue)
    app.register_blueprint(combat_course_app.combat_blue)
    app.register_blueprint(cart_app.cart_blue)

    app.register_blueprint(details_app.blue)

    app.register_blueprint(order_app.order_blue)

    app.run(**APP_CONFIG)