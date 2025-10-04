import os
import cv2
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_from_directory

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB max upload

# Secret & debug from environment
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sketch', methods=['POST'])
def sketch():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        sketch_img = make_sketch(img)

        sketch_img_name = filename.rsplit('.', 1)[0] + "_sketch.jpg"
        sketch_path = os.path.join(app.config['UPLOAD_FOLDER'], sketch_img_name)
        cv2.imwrite(sketch_path, sketch_img)

        return render_template('home.html',
                               org_img_name=filename,
                               sketch_img_name=sketch_img_name)
    return render_template('home.html', error="Invalid file type!")


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
