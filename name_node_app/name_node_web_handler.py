from flask import Flask, request, jsonify
import redis
import uuid
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/register_file_server', methods=['POST'])
def register_file_server():
    ip = request.form.get('ip')
    port = request.form.get('port')
    memsize = request.form.get('memsize')

    server_id = str(uuid.uuid4())
    r.hset("file_servers", server_id, json.dumps({"ip": ip, "port": port, "memsize": memsize}))

    return jsonify({"server_id": server_id}), 201


@app.route('/file', methods=['POST'])
def allocate_file_servers():
    file_size = int(request.form.get('size'))
    filename = str(uuid.uuid4())

    servers = r.hgetall("file_servers")
    allocated_servers = []

    for server_id, server_info in servers.items():
        server_data = json.loads(server_info)
        if int(server_data["memsize"]) >= file_size:
            allocated_servers.append({"server_id": server_id, "ip": server_data["ip"], "port": server_data["port"]})
            r.hset("files", filename, json.dumps({"size": file_size, "servers": allocated_servers}))

            return jsonify({"filename": filename, "servers": allocated_servers}), 200

    return jsonify({"error": "No available servers for the specified file size"}), 400


@app.route('/file/<filename>', methods=['GET'])
def get_file_servers(filename):
    file_info = r.hget("files", filename)

    if file_info:
        file_data = json.loads(file_info)
        return jsonify({"filename": filename, "servers": file_data["servers"]}), 200

    return jsonify({"error": "File not found"}), 404


@app.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_info = r.hget("files", filename)

    if file_info:
        file_data = json.loads(file_info)
        r.hdel("files", filename)
        return jsonify({"filename": filename, "servers": file_data["servers"]}), 200

    return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)