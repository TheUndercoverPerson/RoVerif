from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

ROBLOX_API_URL = 'https://api.roblox.com'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify', methods=['POST'])
def verify():
    username = request.form['username']
    
    # Fetch user data from Roblox API
    user_data = fetch_user_data(username)
    
    if user_data:
        # Generate a verification token (you can use a more secure method)
        verification_token = '123456'  # Change this to a secure method
        
        # Send verification token to user's Roblox account (simulate here)
        send_verification_to_roblox(username, verification_token)
        
        # Render the verify template with username and token
        return render_template('verify.html', username=username, token=verification_token)
    else:
        flash('User not found. Please enter a valid Roblox username.', 'error')
        return redirect(url_for('index'))


def fetch_user_data(username):
    try:
        response = requests.get(f'{ROBLOX_API_URL}/users/get-by-username?username={username}')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def send_verification_to_roblox(username, token):
    # Simulate sending token to user's Roblox account (replace with actual implementation)
    print(f'Sending verification token {token} to {username}')


if __name__ == '__main__':
    app.run(debug=True)
