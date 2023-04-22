from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    message = data['data']['message']
    response_data = {
        'command': '/shrug',
        'message': f'{message} ¯\_(ツ)_/¯'
    }
    return jsonify({'data': response_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060)

# if __name__ == '__main__':
#     shrug_server.run(port=5051)