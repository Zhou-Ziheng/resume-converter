import io
import logging
import sys
import zipfile
from flask import Flask, request, send_file
import requests
from src.convert import convert_resume_handler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define a file handler to log to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/v1/convert', methods=['POST'])
def convert_resume():

    # Check if a file was uploaded in the request
    if 'file' not in request.files:
        logging.error('No file part in the request')
        return 'No file part in the request', 400
    
    file = request.files['file']
    logging.info(f'File uploaded: {file}')
    tex, pdf = convert_resume_handler(file)
    logging.info(f'File created')
    tex_buffer = io.BytesIO(tex)
    pdf_buffer = io.BytesIO(pdf)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the .tex file to the zip archive
        zipf.writestr('resume.tex', tex_buffer.getvalue())
        # Add the .pdf file to the zip archive
        zipf.writestr('resume.pdf', pdf_buffer.getvalue())

    zip_buffer.seek(0)

    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='resume.zip')

if __name__ == '__main__':
    app.run()