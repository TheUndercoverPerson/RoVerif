from flask import Flask, render_template, request, jsonify
import requests
import random
import string

app = Flask(__name__)

# Route to render index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate a random string
@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        username = request.form['username']
        random_string = generate_random_string()
        return jsonify({'random_string': random_string})

# Route to get user ID by username
@app.route('/get_user_id', methods=['POST'])
def get_user_id():
    if request.method == 'POST':
        username = request.form['username']
        user_id = find_user_id(username)
        return jsonify({'user_id': user_id})

# Route to verify the string in Roblox profile description
@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST':
        username = request.form['username']
        roblox_username = request.form['roblox_username']
        success = verify_description(username, roblox_username)
        return jsonify({'success': success})

def generate_random_string():
    characters = string.ascii_letters + string.digits + '⚡🎮🎯'
    return ''.join(random.choice(characters) for _ in range(20))

def find_user_id(username):
    api_url = f'https://api.roblox.com/users/get-by-username?username={username}'
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        if 'Id' in user_data:
            return user_data['Id']
    return None

def verify_description(username, roblox_username):
    api_url = f'https://api.roblox.com/users/get-by-username?username={roblox_username}'
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        if 'Id' in user_data:
            user_id = user_data['Id']
            profile_url = f'https://www.roblox.com/users/{user_id}/profile'
            profile_response = requests.get(profile_url)
            if profile_response.status_code == 200:
                profile_data = profile_response.text
                return username.lower() in profile_data.lower()
    return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
