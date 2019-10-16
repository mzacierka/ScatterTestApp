from flask import Blueprint, render_template, redirect, url_for
about = Blueprint('about', __name__)


@about.route('/about')
def index_view():
    return render_template('About/about.html')




