import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from waitress import serve

from src.converter import OFXConverter


ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
TEMPLATES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES'] = TEMPLATES


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files.get('File', None)
        if not file:
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Excel to OFX Converter</title>
    <h1>OFX Converter</h1>
    <p>Upload neon month statement to convert to ofx</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=File>
      <br/>
      <br/>
      <input type=submit value=Process>
    </form>
    <br/>
    <br/>
    <p><a href="https://christiannogueira.github.io/">Christian Stickel Nogueira</a></p>
    '''


@app.route('/files/<filename>')
def uploaded_file(filename):
    ofx = OFXConverter(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        os.path.join(app.config['TEMPLATES'], 'ofx-template.xml'),
    )

    ofx.create()
    return send_from_directory(app.config['UPLOAD_FOLDER'], ofx.output_file_name, as_attachment=True)


if __name__ == "__main__":
    host, port = "0.0.0.0", 8080
    serve(app, host=host, port=port)
