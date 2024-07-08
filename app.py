from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import random
import string
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

API_ENDPOINT = "https://users.roblox.com/v1/usernames/users"
PROFILE_URL_TEMPLATE = "https://www.roblox.com/users/{user_id}/profile"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify', methods=['POST'])
def verify():
    username = request.form.get('username')
    
    if not username:
        flash('Username is required.', 'error')
        return redirect(url_for('index'))

    # Fetch user ID from Roblox API
    user_id = fetch_user_id(username)
    
    if user_id:
        # Generate a random verification token
        verification_token = generate_random_token()
        
        # Store the token and user ID in session for later verification
        session['verification_token'] = verification_token
        session['username'] = username
        session['user_id'] = user_id
        
        # Render the verify template with username and token
        return render_template('verify.html', username=username, token=verification_token)
    else:
        flash('User not found or banned. Please enter a valid Roblox username.', 'error')
        return redirect(url_for('index'))


@app.route('/check_verification', methods=['POST'])
def check_verification():
    username = session.get('username')
    user_id = session.get('user_id')
    stored_token = session.get('verification_token')
    
    if not username or not user_id or not stored_token:
        flash('Verification session expired. Please try again.', 'error')
        return redirect(url_for('index'))

    profile_url = PROFILE_URL_TEMPLATE.format(user_id=user_id)
    profile_content = fetch_profile_content(profile_url)
    
    if stored_token in profile_content:
        flash(f'Verification successful for user: {username}', 'success')
    else:
        flash('Verification failed. Please ensure the token is added to your profile and try again.', 'error')
    
    return redirect(url_for('index'))


def fetch_user_id(username):
    request_payload = {
        "usernames": [username],
        "excludeBannedUsers": True
    }
    try:
        response = requests.post(API_ENDPOINT, json=request_payload)
        if response.status_code == 200 and response.json()["data"]:
            return response.json()["data"][0]["id"]
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def generate_random_token(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def fetch_profile_content(profile_url):
    try:
        response = requests.get(profile_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return ""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='4000')
