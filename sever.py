# -*-coding:utf-8-*-
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import predict

UPLOAD_FOLDER = 'uploader'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False


@app.route('/test')
def hello():
    return "hello world"


# 检查文件类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path = file_path.replace('\\', '/')  # 解决windows下路径问题
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            file.save(file_path)
            print(file_path)
            result = predict.predict(file_path)
            return jsonify({'signal': 1, 'result': result, 'img_path': file_path})
    else:
        return render_template('index.html')


@app.route('/uploader/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)