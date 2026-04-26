from flask import Flask, render_template, request, send_from_directory
import os

# Correct package imports
from app.modules.data_loader import load_dataset
from app.modules.analytics_engine import analyze_data

app = Flask(__name__)

# -----------------------------
# Folders
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CLEANED_FOLDER = os.path.join(BASE_DIR, 'cleaned_data')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLEANED_FOLDER'] = CLEANED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return 'No file uploaded'

    file = request.files['file']

    if file.filename == '':
        return 'No file selected'

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    # Load dataset
    df = load_dataset(filepath)

    # Analyze dataset
    results = analyze_data(
        df,
        original_filename=file.filename
    )

    return render_template(
        'dashboard.html',

        raw_kpis=results['raw_kpis'],
        cleaned_kpis=results['cleaned_kpis'],
        quality=results.get('quality'),

        charts=results['charts'],
        cleaned_file=results.get('cleaned_file')
    )


@app.route('/download/<path:filename>')
def download_file(filename):

    return send_from_directory(
        app.config['CLEANED_FOLDER'],
        filename,
        as_attachment=True
    )


# -----------------------------
# Run App
# -----------------------------

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
