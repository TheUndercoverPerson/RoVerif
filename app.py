from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import random
import string
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        username = request.form['username']
        random_string = generate_random_string()
        return jsonify({'random_string': random_string})

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

def verify_description(username, roblox_username):
    # Get user ID from Roblox API
    api_url = f'https://api.roblox.com/users/get-by-username?username={roblox_username}'
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        if 'Id' in user_data:
            user_id = user_data['Id']
            # Get profile description
            profile_url = f'https://www.roblox.com/users/{user_id}/profile'
            profile_response = requests.get(profile_url)
            if profile_response.status_code == 200:
                profile_data = profile_response.text
                return username in profile_data.lower()  # Check if username is in profile description
    return False

if __name__ == '__main__':
    app.run(debug=True)
