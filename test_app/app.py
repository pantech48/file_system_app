from flask import Flask, request, jsonify
from celery import Celery
import os

from config import Config
from celery_worker import send_email_task

app = Flask(__name__)
app.config.from_object(Config)





@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    email_data = {
        'subject': 'File Uploaded',
        'recipients': ['recipient@example.com'],
        'body': f'File {file.filename} has been uploaded.',
    }
    send_email_task.delay(email_data)
    return jsonify({"message": "File uploaded"}), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        email_data = {
            'subject': 'File Downloaded',
            'recipients': ['recipient@example.com'],
            'body': f'File {filename} has been downloaded.',
        }
        send_email_task.delay(email_data)
        return jsonify({"message": "File downloaded"}), 200
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
