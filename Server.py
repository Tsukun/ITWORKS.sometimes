import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/averoma/ITWORKS.sometimes/uploads'
ALLOWED_EXTENSIONS = set(['mp3'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploaded')
def uploaded():
    return render_template('load.html')


@app.route('/', methods=['GET', 'POST'])
def render():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('uploaded'))

    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
