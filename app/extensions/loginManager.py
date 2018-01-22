from flask_login import LoginManager

from app.models.user import user

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return user()
