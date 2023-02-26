from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    all_data = data['data']
    message = all_data['message']

    if message.startswith('/'):
        message_data = message.split(' ', 1)
        command = message_data[0][1:]
        if len(message_data) > 1: 
            message = message_data[1]
        else:
            message = ''
    else:
        command = None

    response = {
        'command': command,
        'message': message
    }

    return jsonify({'data': response})


if __name__ == '__main__':
    app.run()
