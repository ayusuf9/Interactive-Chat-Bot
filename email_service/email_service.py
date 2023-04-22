import os
import json
from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get("FROM_EMAIL")
    
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    email_data = data['data']
    recipient = email_data['recipient']
    subject = email_data['subject']
    message = email_data['message']

    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipient,
            subject=subject,
            plain_text_content=message
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({"data": {"status_code": response.status_code, "message": "Email sent"}}), 200

    except Exception as e:
        print(f"SendGrid API Key: {SENDGRID_API_KEY}")  # Add this line
        print(f"Error response body: {e.body}")  # Add this line
        return jsonify({"data": {"status_code": 400, "message": f"Error: {e}"}}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
