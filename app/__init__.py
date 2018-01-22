from flask import Flask
from app.extensions.db import db
from app.controller.public import bp_public
from app.controller.admin import bp_admin
from app.controller.auth import bp_auth
from app.controller.error import bp_error
from app.logger import init_logger
from app.extensions.templatefilters import init_templatefilter
from app.extensions.loginManager import login_manager
from app.task.tasks import randonpicture


def create_app(config, should_register_blueprints=True):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)

    init_templatefilter(app)
    init_logger(app)

    app.config['PICTURENUM'] = randonpicture(app.config['APP_PATH'] + '/app/static/picture')

    if should_register_blueprints:
        register_blueprints(app)

    with app.app_context():
        db.create_all()
    return app


def register_blueprints(app):

    app.register_blueprint(bp_public)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_error)
