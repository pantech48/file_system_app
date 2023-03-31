from flask import Flask, request, jsonify, abort
import os
import shutil
from pathlib import Path
import jwt
from flasgger import Swagger, swag_from
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_service import FileSystem
from logs.logger import logger
from config.config_parser import config

app = Flask(__name__)
swagger = Swagger(app)
f_s = FileSystem()
HOST = "localhost"
PORT = 5001
MEMORY_SIZE = 40960


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Api-Key", "")
        if not token:
            return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        try:
            user_id = jwt.decode(token, config()["AUTH"]["secret_key"], algorithms="HS256")['user_id']
            user_folder = Path(FileSystem.FILE_STORAGE_PATH) / str(user_id)
            Path.mkdir(user_folder, exist_ok=True)
            os.chdir(user_folder)
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        return f(*args, **kwargs)
    return wrapper


@token_required
@app.route('/files/list', methods=['GET'])
def get_files_with_metadata():
    """
    Get the list of files with metadata.
    ---
    tags:
      - Files
    responses:
      200:
        description: List of files with metadata
        schema:
          type: object
          properties:
            file_names:
              type: array
              items:
                type: string
            files:
              type: array
              items:
                type: object
                properties:
                  size:
                    type: integer
                    format: int64
                  last_modified:
                    type: string
                  creation_time:
                    type: string
    """
    file_names = os.listdir(FileSystem.FILE_STORAGE_PATH)
    files_path = [os.path.join(FileSystem.FILE_STORAGE_PATH, file) for file in file_names]
    files = [f_s.get_metadata(file) for file in files_path]
    logger.info(f"Received request for files list. Files: {file_names}")
    response = jsonify(file_names, files)
    logger.info(f"Returning list of files with metadata: {response}")
    return response, 200


@token_required
@app.route('/files/<filename>', methods=['GET'])
def get_file_content_with_metadata(filename: str):
    """
    Get file content and metadata by filename.
    ---
    tags:
      - Files
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the file
    responses:
      200:
        description: File content and metadata
        schema:
          type: object
          properties:
            filename:
              type: string
            content:
              type: string
            metadata:
              type: object
              properties:
                size:
                  type: integer
                  format: int64
                last_modified:
                  type: string
                creation_time:
                  type: string
      404:
        description: File not found
    """
    logger.info(f"Received request for file: {filename}")
    files_storage = FileSystem.FILE_STORAGE_PATH
    file_names = os.listdir(files_storage)
    if filename in file_names:
        path = os.path.join(FileSystem.FILE_STORAGE_PATH, filename)
        content = f_s.read_file(path)
        metadata = f_s.get_metadata(path)
        response = jsonify({'filename': filename,
                            'content': content.decode('utf-8'),
                            'metadata': metadata})
        return response, 200
    else:
        err_massage = f"File {filename} not found."
        logger.error(err_massage)
        abort(404, err_massage)


@token_required
@app.route('/files', methods=['POST'])
@swag_from({
    'tags': ['files'],
    'summary': 'Create a new file',
    'description': 'Creates a new file with content from the request body and returns a JSON with the filename.',
    'parameters': [
        {
            'in': 'body',
            'name': 'content',
            'description': 'File content',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'content': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'File created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'filename': {'type': 'string'}
                }
            }
        },
        '400': {'description': 'Bad request'}
    }
})
def create_file():
    """Creates file with content from request body. Returns JSON with filename."""
    logger.info("Received request for file creation.")
    if request.content_type != 'application/json':
        err_massage = "Content-Type must be 'application/json'."
        logger.error(err_massage)
        abort(400, err_massage)

    data = request.get_json()
    if 'content' not in data:
        err_massage = "Key 'content' is missing."
        logger.error(err_massage)
        abort(400, err_massage)

    content = data['content']
    filename = f_s.create_file(content.encode('utf-8'))
    response = jsonify({'filename': filename})
    return response, 201


@token_required
@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename: str):
    """Deletes file with name from request body. Returns JSON with filename."""
    logger.info(f"Received request for file deletion: {filename}")
    files_storage = FileSystem.FILE_STORAGE_PATH
    path = os.path.join(files_storage, filename)
    if os.path.exists(path):
        f_s.delete_file(path)
        return jsonify({'filename': path}), 200
    else:
        err_massage = f"File {filename} not found."
        logger.error(err_massage)
        abort(404, err_massage)


@token_required
@app.route('/change_file_dir', methods=['POST'])
def change_file_directory():
    """ Changes file directory. Returns JSON with new path."""
    logger.info("Received request for file directory change.")
    if request.content_type != 'application/json':
        err_massage = "Content-Type must be 'application/json'."
        logger.error(err_massage)
        abort(400, err_massage)

    data = request.get_json()
    if 'path' not in data:
        err_massage = "Key 'path' is missing."
        logger.error(err_massage)
        abort(400, err_massage)

    path = data['path']

    try:
        destination_folder, filename = os.path.split(path)
        logger.info(f"Path: {path}, new folder: {destination_folder}, filename: {filename}")
        search_dir = Path(config()["APP"]["working_directory"])
        matches = search_dir.glob(f"**/{filename}")
        match = [file for file in matches]
        if len(match) > 1:
            err_massage = f"File {filename} is not unique."
            logger.error(err_massage)
            abort(400, err_massage)
        elif len(match) == 0:
            err_massage = f"File {filename} not found."
            logger.error(err_massage)
            abort(404, err_massage)
        else:
            original_path = match[0]
            shutil.move(original_path, path)
            logger.info(f"File {filename} moved from {original_path} to {path}")

        logger.info(f"File directory changed to: {path}")
        return jsonify({'path': path}), 200
    except OSError as e:
        err_massage = f"Path {path} is not valid. {e}"
        logger.error(err_massage)
        abort(400, err_massage)


@app.route('/server_info', methods=['GET'])
def get_server_info():
    """Returns JSON with server info."""
    logger.info("Received request for server info.")
    response = jsonify({'host': HOST,
                        'port': PORT,
                        'memory_size': MEMORY_SIZE})
    logger.info(f"Returning server info: {response}")
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)
