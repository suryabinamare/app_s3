# app.py
from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__)

S3_BUCKET = "surya-app"
AWS_ACCESS_KEY = "AKIA6HSCUECSJQ6SF7FS"
AWS_SECRET_KEY = "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"

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            s3.upload_file(file_path, S3_BUCKET, file.filename)
            return redirect(url_for('index'))
        except NoCredentialsError:
            return 'Credentials not available.'
    else:
        return 'File type not allowed.'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)
