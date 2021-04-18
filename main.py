from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
import extract_images
import os
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "shashank secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/convert",  methods = ['GET', 'POST'])
def convert_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            print("sssss")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("ddddd")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("qqq")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extract_images.convert_pdf(filename)
            return send_file(f"work/{filename[:-4]}/{filename}", as_attachment=True)
            # return redirect('/')
        
    return render_template('error.html', msg = "file type not supported")


@app.route("/")
def index():
    # extract_images.convert_pdf('sample.pdf')
    return render_template('hello.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)