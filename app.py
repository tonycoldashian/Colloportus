import os 
from flask import Flask, request, render_template, flash, redirect, send_file, url_for
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from zipfile import ZipFile
import shutil



app = Flask(__name__, static_folder = 'static')

app.config['UPLOAD_FOLDER']         = os.path.join(app.root_path, 'uploads')
app.config['DOWNLOAD_FOLDER']       = os.path.join(app.root_path, 'downloads')
app.config['MAX_CONTENT_LENGTH']    = 16 * 1024 * 1024

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWLOAD_FOLDER'])
    
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
        
def load_key(key_path):
    return open(key_path, 'rb').read()


@app.route('/')
def index():
    return render_template('index.html')
