from flask import Flask, render_template, request
import os
from mask import mask_sensitive_info

app = Flask(__name__)

# Folder to store uploaded and masked images
UPLOAD_FOLDER = 'static/masked'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Max 10 MB

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            print("⚠ No image part in the form.")
            return render_template('index.html', masked_image=None)

        file = request.files['image']

        if file.filename == '':
            print("⚠ No file selected.")
            return render_template('index.html', masked_image=None)

        if file and allowed_file(file.filename):
            filename = file.filename
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"masked_{filename}")

            file.save(input_path)
            print(f"✅ File saved: {input_path}")

            # ✅ Correct usage with both input and output paths
            mask_sensitive_info(input_path, output_path)
            print(f"✅ Masked image saved: {output_path}")

            return render_template('index.html', masked_image=output_path)

        else:
            print("❌ Invalid file type.")
            return render_template('index.html', masked_image=None)

    return render_template('index.html', masked_image=None)

if __name__ == '__main__':
    app.run(debug=True)