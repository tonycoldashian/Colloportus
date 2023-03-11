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
    os.makedirs(app.config['DOWNLOAD_FOLDER'])
    
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
        
def load_key(key_path):
    return open(key_path, 'rb').read()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    #check if the post request has the file part
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected"
    
    # Allowable file types
    if file and allowed_file(file.filename):
        # secure the filename
        filename = secure_filename(file.filename)
        
        #saving file to upload folder
        filepath = os.path.join(app.comfig['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generating a enc_key as 'key.key'
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
            
        # Create a Fernet instance with generated key
        fernet = Fernet(key)
        
        # Reading contents from original file
        with open(filepath, 'rb') as original_file:
            original = original_file.read()
            
        # Encrpyt the file
        encrypted = fernet.encrypt(original)
        
        # saving enc_contents to a file
        with open(filename, 'wb') as encryped_file:
            encryped_file.write(encrypted)
            
        # Create a zip file contaning the enc_file and enc_key
        filen = filename.split(".")[0]
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filen + '.zip')
        with ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(filename)
            zip_file.write('key.key')
        zip_file.close()
        
        # Remove the original file, enc_file and the enc_key
        os.remove(filename)
        os.remove(filepath)
        os.remove('key.key')
        
        # Send the file to the user
        response = send_file(zip_path, as_attachment=True)
        
        return response
    
    else:
        # File type not allowed
        return render_template('index.html')
            










def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}