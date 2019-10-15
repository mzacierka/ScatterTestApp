from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def index_view():
    return render_template('Login/login_page.html')
    

@main.route('/forget_pw')
def reset_view():
    return render_template('Login/forget_pw.html')

@main.route('/reset_pw')
def reset1_view():
    return render_template('Login/reset_pw.html')

@main.route('/download_page')
def reset2_view():
    return render_template('Login/download_page.html')

@main.route('/search')
def reset3_view():
    return render_template('Login/search.html')    


@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)

