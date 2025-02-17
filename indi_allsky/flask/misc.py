from functools import wraps

from flask import current_app

from flask_login import current_user


def login_optional(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"):
            pass
        elif not current_app.config.get('INDI_ALLSKY_AUTH_ALL_VIEWS'):
            # allow some views to be unauthenticated
            pass
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view

