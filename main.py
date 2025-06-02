from flask import Flask, request, jsonify
import random

app = Flask(__name__)

import os
API_KEY = os.environ.get("API_KEY", "")

def extract_initials(full_name):
    parts = full_name.strip().split()
    if len(parts) == 0:
        return "XXX"
    initials = ''.join([p[0].upper() for p in parts])
    return initials[:3].ljust(3, 'X')

@app.route('/generate-id', methods=['POST'])
def generate_id():
    # 🔐 Check for API key in request headers
    client_key = request.headers.get('x-api-key')
    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    academy_code = data.get("academy_code", "WSS").upper()
    full_name = data.get("full_name", "")

    initials = extract_initials(full_name)
    rand_number = str(random.randint(1000, 9999))
    student_id = f"{academy_code}{initials}{rand_number}"

    return jsonify({"student_id": student_id})

if __name__ == '__main__':
    app.run()

