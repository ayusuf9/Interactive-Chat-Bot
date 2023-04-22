import json
import requests
import psycopg2
import time

from flask import Flask, request, jsonify

app = Flask(__name__)

command_mapping = {}

def get_db_connection():
    return psycopg2.connect(
        dbname="chatbot",
        user="chatbot",
        password="chatbot_password",
        host="postgres_container",
        port="5432"
    )

def save_command_mapping(command: str, server_url: str):
    command_mapping[command] = server_url
    with open("serverMapping.json", "w") as f:
        json.dump(command_mapping, f)

def load_command_mapping():
    try:
        with open("serverMapping.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

command_mapping = load_command_mapping()

@app.route('/message', methods=['POST'])
def message():
    try:
        data = request.get_json()
        all_data = data['data']
        message = all_data['message'].strip()

        if not message:
            return jsonify({"data": {"command": None, "message": "Error: Empty input"}}), 400

        if message.startswith('/'):
            message_data = message.split(' ', 1)
            command = message_data[0][1:]
            if len(message_data) > 1: 
                message = message_data[1].strip()
            else:
                message = ''
        else:
            command = None

        if command:
            if command in command_mapping:
                server_url = command_mapping[command]
                if not server_url.endswith("/"):
                    server_url += "/"
                response = requests.post(f"{server_url}execute", json={"data": {"command": command, "message": message}})
                response_data = response.json()["data"]
            elif command == "shrug":
                response_data = {
                    'command': command,
                    'message': f"{message} ¯\_(ツ)_/¯"
                }
            else:
                response_data = {
                    'command': command,
                    'message': message if message else "Invalid command"
                }
        else:
            response_data = {
                'command': command,
                'message': message if message else "Invalid command"
            }

        return jsonify({'data': response_data}), 200
    except:
        return jsonify({"data": {"command": None, "message": "Error: Invalid input"}}), 400

@app.route('/register', methods=['POST'])
def register_command():
    data = request.get_json()
    command_data = data['data']
    command = command_data['command']
    server_url = command_data['server_url']

    save_command_mapping(command, server_url)
    return jsonify({'data': {'command': command, 'message': 'saved'}}), 200

register_data = {
    "data": {
        "command": "email",
        "server_url": "http://email_service:5051"
    }
}

def register_email_command():
    response = requests.post("http://chatbot_parser:5050/register", json=register_data)
    print("Email command registration response:", response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, threaded=True)

    # Add a delay before making the registration request.
    time.sleep(5)
    register_email_command()
