from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from src.utils.audio_convert import convert_audio, SUPPORTED_FORMATS, BITRATES
from src.utils.batch_convert import batch_convert
from src.utils.clean_name import clean_file_name
from src.utils.data_ingest import save_uploaded_file
from pathlib import Path
from zipfile import ZipFile
import tempfile
import logging

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 700 * 1024 * 1024
logging.basicConfig(level=logging.INFO) 

def convert_and_save(file, fmt, bitrate, normalize):
    input_path = save_uploaded_file(file)
    output_name = input_path.stem
    return convert_audio(
        input_path, fmt, bitrate,
        normalize=normalize,
        output_name=output_name
    )


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", formats=SUPPORTED_FORMATS, bitrates=BITRATES)

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("files")
    fmt = request.form.get("format")
    bitrate = request.form.get("bitrate", "192k")
    normalize = request.form.get("normalize") == "on"
    
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    temp_dir = Path(tempfile.mkdtemp())
    converted, skipped = [], []

    for file in files:
        try:
            out_path = convert_and_save(file, fmt, bitrate, normalize)
            converted.append(out_path)
        except Exception as e:
            logging.warning(f"Skipping {file.filename}: {e}")
            skipped.append({"filename": file.filename, "error": "Conversion failed"})

    if not converted:
        return jsonify({
            "error": "No valid files to convert.",
            "skipped": skipped
        }), 400

    if len(converted) == 1 and converted[0].is_file():
        return send_file(converted[0], as_attachment=True)

    # Multiple files: Zip output
    zip_path = temp_dir / "converted_audio.zip"
    with ZipFile(zip_path, "w") as zipf:
        for f in converted:
            zipf.write(f, arcname=f.name)

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)