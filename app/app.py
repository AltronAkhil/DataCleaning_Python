from flask import Flask, render_template, request, send_from_directory
import os

from modules.data_loader import load_dataset
from modules.analytics_engine import analyze_data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

    # Load raw dataset only
    df = load_dataset(filepath)

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

    cleaned_folder = os.path.join(app.root_path, 'cleaned_data')

    return send_from_directory(
        cleaned_folder,
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)