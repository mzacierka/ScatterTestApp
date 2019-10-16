from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from FlaskAPP.endpoints.Login.forms import LoginForm
settings = Blueprint('settings', __name__)


@login_required
@settings.route('/settings')
def settings_view():
    if current_user.is_authenticated:
        return render_template('Settings/settings.html', user=current_user)
    else:
        return render_template('Login/login.html', form=LoginForm())
