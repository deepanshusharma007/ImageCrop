import os
from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get user-specified upload and cropped folders
        upload_folder = request.form.get('upload_folder')
        cropped_folder = request.form.get('cropped_folder')

        # Set upload and cropped folders if provided
        app.config['UPLOAD_FOLDER'] = upload_folder
        app.config['CROPPED_FOLDER'] = cropped_folder

        # Process each uploaded file
        cropped_filenames = []
        for file in request.files.getlist('files'):
            if file.filename == '':
                continue

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                try:
                    file.save(filepath)
                except Exception as e:
                    print(f"Error saving uploaded file: {e}")
                    continue

                # Get form data
                height = int(request.form.get('height'))
                width = int(request.form.get('width'))
                quality = int(request.form.get('quality'))

                # Perform image cropping
                try:
                    with Image.open(filepath) as img:
                        cropped_img = img.crop((0, 0, width, height))
                        cropped_img_path = os.path.join(app.config['CROPPED_FOLDER'], f'cropped_{filename}')
                        cropped_img.save(cropped_img_path, quality=quality)
                        cropped_filenames.append(f'cropped_{filename}')
                except Exception as e:
                    print(f"Error cropping {filename}: {e}")

        return render_template('upload_complete.html', cropped_filenames=cropped_filenames)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9090)
