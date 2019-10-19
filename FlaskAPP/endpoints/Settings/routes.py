import os
from flask import Flask, Blueprint, send_from_directory, render_template, redirect, url_for, flash, request, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from FlaskAPP.config import Config
from FlaskAPP.endpoints.Login.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from FlaskAPP.models.jsonfiles import JSONFiles
from FlaskAPP import db
from io import BytesIO
settings = Blueprint('settings', __name__)
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['json'])
# defines folder for uploads
UPLOAD_FOLDER = 'FlaskAPP/static/json'          
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@login_required
@settings.route('/settings/upload')
def show():
    if current_user.is_authenticated:
        return render_template('Settings/fileUpload.html', user=current_user)
    else:
        return render_template('Login/login.html', form=LoginForm())

# The upload feature. Routes to uploaded_file upon successful completion
@login_required
@settings.route('/settings/upload/uploadFile', methods=['POST'])
def upload_file():

    file = request.files['file']

    db.session.rollback()
    newFile = JSONFiles(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()

    return '<p>Saved ' + file.filename + ' to the database! <a href="/settings"> Return to settings </a>'
    

# Displays JSON downloads
@login_required
@settings.route('/settings')
def show_table():
    if current_user.is_authenticated:
        return render_template('Settings/settings.html', user=current_user, file_data = JSONFiles.query.order_by(JSONFiles.name).all())
    else:
        return render_template('Login/login.html', form=LoginForm())

@login_required
@settings.route('/settings/download/<filename>')
def download(filename):
    file_data = JSONFiles.query.filter_by(name=filename).first()
    return send_file(BytesIO(file_data.data), attachment_filename=filename, as_attachment=True)

# @login_required
# @settings.route('/settings')
# def settings_view():
#     if current_user.is_authenticated:
#         return render_template('Settings/settings.html', user=current_user)
#     else:
#         return render_template('Login/login.html', form=LoginForm())