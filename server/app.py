import os
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")
PASSWORD = "2427"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    """Serve the frontend index.html."""
    return send_from_directory(os.path.abspath(APP_DIR), "index.html")


@app.route("/api/upload", methods=["POST"])
def upload_csv():
    """Receive a CSV file upload after password verification."""
    password = request.form.get("password", "")
    if password != PASSWORD:
        return jsonify({"error": "密码错误"}), 403

    csv_file = request.files.get("file")
    if csv_file is None:
        return jsonify({"error": "未提供文件"}), 400

    filename = csv_file.filename or ""
    if not filename.endswith(".csv"):
        return jsonify({"error": "仅支持 CSV 文件"}), 400

    # Sanitize filename
    safe_name = "".join(
        c for c in filename if c.isalnum() or c in ("_", "-", ".")
    )
    if not safe_name:
        safe_name = datetime.datetime.now().strftime("upload_%Y%m%d_%H%M%S.csv")

    save_path = os.path.join(UPLOAD_DIR, safe_name)

    # Avoid overwriting: append counter if file exists
    base, ext = os.path.splitext(safe_name)
    counter = 1
    while os.path.exists(save_path):
        save_path = os.path.join(UPLOAD_DIR, f"{base}_{counter}{ext}")
        counter += 1

    csv_file.save(save_path)
    saved_name = os.path.basename(save_path)
    return jsonify({"message": "上传成功", "filename": saved_name}), 200


@app.route("/api/files", methods=["GET"])
def list_files():
    """List all uploaded CSV files."""
    password = request.args.get("password", "")
    if password != PASSWORD:
        return jsonify({"error": "密码错误"}), 403

    files = []
    for f in sorted(os.listdir(UPLOAD_DIR), reverse=True):
        if f.endswith(".csv"):
            path = os.path.join(UPLOAD_DIR, f)
            stat = os.stat(path)
            files.append({
                "filename": f,
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat(),
            })
    return jsonify({"files": files}), 200


@app.route("/api/files/<filename>", methods=["GET"])
def download_file(filename):
    """Download a specific CSV file."""
    password = request.args.get("password", "")
    if password != PASSWORD:
        return jsonify({"error": "密码错误"}), 403

    # Prevent path traversal
    safe = os.path.basename(filename)
    if not os.path.isfile(os.path.join(UPLOAD_DIR, safe)):
        return jsonify({"error": "文件不存在"}), 404

    return send_from_directory(UPLOAD_DIR, safe, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
