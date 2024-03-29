from apps import app
from flask_cors import CORS
from views import user_app, cart_app, details_app, mine_app, free_course_app, \
    combat_course_app, order_app, person_app, person_combat_course_app,collect_app,\
    person_course_app,global_search_app



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
    app.register_blueprint(person_app.blue)
    app.register_blueprint(person_combat_course_app.blue)
    app.register_blueprint(collect_app.collect_blue)
    app.register_blueprint(person_course_app.per_course_blue)
    app.register_blueprint(global_search_app.search_blue)

    app.run(**APP_CONFIG)