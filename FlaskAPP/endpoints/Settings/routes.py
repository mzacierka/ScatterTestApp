import os
from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from FlaskAPP.config import Config
from FlaskAPP.endpoints.Login.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from FlaskAPP.models.jsonfiles import JSONFiles
from FlaskAPP import db
from io import BytesIO


settings = Blueprint('settings', __name__)
app = Flask(__name__)
ALLOWED_EXTENSIONS = {'json'}

# The upload feature. Routes to uploaded_file upon successful completion
@login_required
@settings.route('/settings/upload')
def show():
    if current_user.is_authenticated:
        return render_template('Settings/fileUpload.html', user=current_user)
    else:
        return render_template('Login/login.html', form=LoginForm())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Landing page upon successful upload, needs to be changed
@login_required
@settings.route('/settings/upload/uploadFile', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/settings')
        file = request.files['file']
        # check if file exists
        if file.filename == '':
            flash('No selected file')
            return redirect('/settings')
        # check if file is an allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Send to database        
            db.session.rollback()
            newFile = JSONFiles(name=file.filename, data=file.read())
            db.session.add(newFile)
            db.session.commit()
        
            flash('Upload Successful')

            return redirect('/settings')
        # exit failure
        flash('File not correct extension')
        return redirect('/settings')

    
    
# Displays JSON downloads
@login_required
@settings.route('/settings')
def show_table():
    if current_user.is_authenticated:
        return render_template('Settings/settings.html', user=current_user, file_data = JSONFiles.query.order_by(JSONFiles.name).all())
    else:
        return render_template('Login/login.html', form=LoginForm())

# Download link for JSON files
@login_required
@settings.route('/settings/download/<filename>')
def download(filename):
    file_data = JSONFiles.query.filter_by(name=filename).first()
    return send_file(BytesIO(file_data.data), attachment_filename=filename, as_attachment=True)
