from flask import Flask, request, jsonify
import os

from file_service import FileSystem
from config.config_parser import config

app = Flask(__name__)
f_s = FileSystem()


@app.route('/files/list', methods=['GET'])
def get_files_with_metadata():
    files = []
    files_dir = os.listdir(f"{config()['APP']['working_directory']}{'files'}")
    for file in files_dir:
        files.append(f_s.get_metadata(file))
    return jsonify(files)


@app.route('/files', methods=['GET'])
def get_file_content_and_metadata(path: str):
    files_dir = os.listdir(f"{config()['APP']['working_directory']}{'files'}")
    if path in files_dir:
        content = f_s.read_file(path)
        metadata = f_s.get_metadata(path)
        return jsonify({'content': content, 'metadata': metadata})


@app.route('/files', methods=['POST'])
def create_file():
    pass


@app.route('/files/<str:path>', methods=['DELETE'])
def delete_file(path):
    files_dir = os.listdir(f"{config()['APP']['working_directory']}{'files'}")
    if path in files_dir:
        f_s.delete_file(path)
    return jsonify({'filename': path})


if __name__ == '__main__':
    app.run(debug=True)