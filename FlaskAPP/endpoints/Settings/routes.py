import os
from flask import Flask, Blueprint, send_from_directory, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from FlaskAPP.config import Config
from FlaskAPP.endpoints.Login.forms import LoginForm
settings = Blueprint('settings', __name__)

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['json'])
UPLOAD_FOLDER = 'FlaskAPP/static/json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# @login_required
# @settings.route('/settings')
# def settings_view():
#     if current_user.is_authenticated:
#         return render_template('Settings/settings.html', user=current_user)
#     else:
#         return render_template('Login/login.html', form=LoginForm())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@settings.route('/settings/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
@login_required
@settings.route('/settings/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('settings.uploaded_file',
                                    filename=filename))
    if current_user.is_authenticated:
        return render_template('Settings/fileUpload.html', user=current_user)
    else:
        return render_template('Login/login.html', form=LoginForm())

@login_required
@settings.route('/settings')
def show_table():
    if current_user.is_authenticated:
        return render_template('Settings/settings.html', user=current_user, tree=make_tree("FlaskAPP/static/json"))
    else:
        return render_template('Login/login.html', form=LoginForm())

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree