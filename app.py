from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/auth/callback', methods=['GET'])
def auth_callback():
    code = request.args.get('code')
    print(f"Authorization code received: {code}")
    return jsonify(message="Authorization successful", code=code), 200

@app.route('/auth/deauthorize', methods=['POST'])
def deauthorize_callback():
    user_id = request.json.get('user_id')
    print(f"User {user_id} has deauthorized the app.")
    return jsonify(message="Deauthorization successful"), 200

@app.route('/auth/delete', methods=['POST'])
def delete_callback():
    user_id = request.json.get('user_id')
    print(f"Received data deletion request for user {user_id}.")
    return jsonify(message="Data deletion successful"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
