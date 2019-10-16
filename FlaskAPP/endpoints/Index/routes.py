from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from FlaskAPP.endpoints.Login.forms import LoginForm
main = Blueprint('main', __name__)


@main.route('/')
def index_view():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    else:
        return render_template('Login/login.html', form=LoginForm())


@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)

