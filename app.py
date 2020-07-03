import os
from flask import Flask, request, flash, redirect, url_for, render_template, send_file
from dicom_to_image import convertImage, get_dicom_data

UPLOAD_FOLDER = 'dicom_images'
ALLOWED_EXTENSIONS = {'dcm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my secret key'


def is_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set the route for the function


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the POST request has the file part
        # Then save the uploaded file
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Chưa chọn file')
            return redirect(request.url)
        elif file and is_allowed(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result_path = convertImage(filepath)
            data = get_dicom_data()
            return render_template('index.html', success=True, data=data, filename='result.png')
    return render_template('index.html', success=False)

# Download file image


@app.route('/download/<string:filename>', methods=['GET'])
def download_image(filename):
    return send_file(filename, as_attachment=True, mimetype='image/png', attachment_filename=filename)
