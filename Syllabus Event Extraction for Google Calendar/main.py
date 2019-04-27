#!/usr/bin/env python3

from flask import Flask, render_template
from werkzeug import secure_filename
from flask import request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'html'])
app.debug = True

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
# @app.route('/uploaded', methods = ['GET', 'POST'])
# def uploaded_file():
#     if request.method == 'POST':
#         submitted_file = request.files['file']
#         if submitted_file and allowed_filename(submitted_file.filename):
#             filename = secure_filename(submitted_file.filename)
#             submitted_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#             file_url = url_for('uploaded_file', filename=filename)
#             return redirect(file_url)

      # f = request.files['file']
      # #f.save(secure_filename(f.filename))
      # print('file uploaded successfully')
      # return render_template('uploaded.html')

@app.route("/uploaded", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash('File uploaded!', 'success')
            print("Loading ", "{}{}".format(UPLOAD_FOLDER, file.filename), " ...")
            process = subprocess.Popen('python3 addEvent.py --filename {}{}'.format(UPLOAD_FOLDER, file.filename), shell=True, stdout=subprocess.PIPE)
            print("Run successfully")
            output, err = process.communicate()
    return render_template('uploaded.html')

		
if __name__ == "__main__":
    app.run(debug=True)
