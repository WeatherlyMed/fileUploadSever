from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER_1 = 'uploads/folder1'
UPLOAD_FOLDER_2 = 'uploads/folder2'
os.makedirs(UPLOAD_FOLDER_1, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_2, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        folder_choice = request.form.get('folder')
        tos_signed = request.form.get('tos')

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if not tos_signed:
            flash('You must agree to the Terms of Service.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if folder_choice == 'folder1':
                save_path = os.path.join(UPLOAD_FOLDER_1, file.filename)
            elif folder_choice == 'folder2':
                save_path = os.path.join(UPLOAD_FOLDER_2, file.filename)
            else:
                flash('Invalid folder choice.')
                return redirect(request.url)

            file.save(save_path)
            flash('File successfully uploaded!')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
