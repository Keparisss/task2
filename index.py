
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory,send_file
from flask import Response
from flask import safe_join
from flask import render_template
import json
import os


UPLOAD_FOLDER = "C:\\Users\\admin\\PycharmProjects\\lab2\\uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def not_found_error(error):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
         <title>Upload new File</title>
         <style>
                body{background-color: pink;}
                h1,p{color: blue;}
                div{ margin : 0 auto; width:800px;text-align: center; height: 350px;}
                input{width:300px; height:50px; color: blue;display: inline-block;}
                form{width:300px; height:50px; color: blue; display: inline-block;}
                
         </style>
    </head>
    <body>
        <div>
             <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
             <input type=submit value=Upload>
        </div>
     </body>
     </html>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
root_path = 'C:\\Users\\admin\\PycharmProjects\\lab2'

@app.route('/path1')
def path1():

    files = os.listdir(root_path)

    for file in files:
       # full_path = safe_join(file)
        return file

@app.route("/ls1")
def dir_viewer():
    entries = os.scandir(root_path)
    render_template("ind.html", entries=entries)
    return """{% for entry in entries %}
           {% if entry.is_file() %}
                <a href="{{ url_for("download_file", path=entry.root_path) }}">{{ entry.name }}</a>
            {% else %}
                <a href="{{ url_for("dir_viewer", path=entry.root_path) }}">{{ entry.name }}</a>
            {% endif %}
          {% endfor %}
           """

@app.route("/download/<path:path>")
def download_file(path):
        return send_file(path)

path='C:/Users/'
@app.route("/ls")
def func(path):
    for root, dirs, files in os.walk(path):
        for file in files:
             print(os.path.join(path,file))
             break

if __name__== '__main__':
    app.run()