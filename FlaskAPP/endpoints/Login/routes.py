from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from FlaskAPP.models.users import Doctor
from FlaskAPP.endpoints.Login.forms import LoginForm, ForgotEmailForm, ResetEmailForm
from FlaskAPP import mail, db
from FlaskAPP.config import Config
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

login = Blueprint('login', __name__)
s = URLSafeTimedSerializer(Config.SECRET_KEY)


@login.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('Login/login.html', form=form)
    else:
        email = form.email.data.strip()
        password = form.password.data

        # Query for a user with the provided username
        result = Doctor.query.filter_by(email=email).first()

        if result is not None and password == result.password_:
            # Login user
            login_user(result)
            return render_template('index.html', user=result)
        else:
            flash('Email or Password is incorrect', 'danger')
            return render_template('Login/login.html', form=form)


@login.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect('login')


@login.route('/forget_pw', methods=['GET', 'POST'])
def forget_pw():
    form = ForgotEmailForm()

    if form.validate_on_submit():
        flash('You will recieve an email if there is an account attached.', 'success')
        recipient_email = form.email.data
        email_exists = Doctor.query.filter_by(email=recipient_email).first()
        if email_exists is not None:
            token = s.dumps(recipient_email, salt='email-confirm')

            msg = Message('Reset Password', recipients=[recipient_email])
            link = url_for('login.reset_pw', token=token, _external=True)
            msg.body = 'Reset your password with this link {}'.format(link)
            mail.send(msg)
            return redirect("login")
    return render_template("Login/forget_pw.html", form=form)


@login.route('/reset_pw/<token>', methods=['GET', 'POST'])
def reset_pw(token):
    form = ResetEmailForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)
        if form.validate_on_submit():
            if form.password_first == form.password_confirm:
                update_user = Doctor.query.filter_by(email=email).first()
                update_user.password_ = form.password_confirm
                db.session.commit()
                flash('Your password has been reset', 'success')
                return redirect("login")
        return render_template('Login/reset_pw.html', form=form)
    except SignatureExpired:
        return 'Token expired'
    except BadTimeSignature:
        render_template('404.html')
    #  return render_template("Login/reset_pw.html")


@login.route('/reset_pw')
def redirect_login():
    return redirect("login")
