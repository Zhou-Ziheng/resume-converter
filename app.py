import io
import logging
import os
import sys
import zipfile
from flask import Flask, request, send_file, jsonify
from src.convert import convert_resume_handler, compile_tex
from flask_cors import CORS
import ddtrace


app = Flask(__name__)
CORS(app)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define a file handler to log to a file
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

# if prod
if os.getenv("ENV") == "prod":
    FORMAT = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
        "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
        "- %(message)s"
    )
else:
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ddtrace.tracer.enabled = False

formatter = logging.Formatter(FORMAT)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/v1/convert", methods=["POST"])
@ddtrace.tracer.wrap()
def convert_resume():
    logging.info(f"Request received: {request.method} {request.path}")
    # Check if a file was uploaded in the request
    if "file" not in request.files:
        logging.error("No file part in the request")
        return "No file part in the request", 400

    file = request.files["file"]
    logging.info(f"File uploaded: {file}")

    tex, pdf = convert_resume_handler(file, request.form.get("style"))
    logging.info(f"File created")

    tex_buffer = io.BytesIO(tex)
    pdf_buffer = io.BytesIO(pdf)

    if request.form.get("getPDF") == "true":
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="resume.pdf",
        )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add the .tex file to the zip archive
        zipf.writestr("resume.tex", tex_buffer.getvalue())
        # Add the .pdf file to the zip archive
        zipf.writestr("resume.pdf", pdf_buffer.getvalue())

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="resume.zip",
    )


def verify_api_key(api_key):
    # Retrieve the valid API key from environment variable
    valid_api_key = os.getenv("PDFLATEX_API_KEY")

    # Check if the provided API key matches the valid API key
    return api_key == valid_api_key if valid_api_key else False


@app.route("/v1/compile", methods=["POST"])
@ddtrace.tracer.wrap()
def compile_latex():
    # Step 1: Verify API Key
    if not verify_api_key(request.headers.get("API-Key")):
        return jsonify({"error": "Unauthorized"}), 401

    # Step 2: Extract LaTeX string from request body
    try:
        latex_string = request.data.decode("utf-8")
    except Exception as e:
        return jsonify({"error": "Invalid request data"}), 400

    if not latex_string:
        return jsonify({"error": "No LaTeX string provided"}), 400

    # Step 3: Call compile_tex function
    try:
        pdf = compile_tex(latex_string)
        pdf_buffer = io.BytesIO(pdf)
        mimetype = "application/pdf"

        return send_file(
            pdf_buffer,
            mimetype=mimetype,
            as_attachment=True,
            attachment_filename="sample.pdf",
        )
    except Exception as e:
        return jsonify({"error": f"Compilation failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
