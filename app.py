from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'mci9ewf8newdsiumd3uqwdnuiaewnf8uwoeciurrfewindimewfm'  # Change this to a secure random key

API_ENDPOINT = "https://users.roblox.com/v1/usernames/users"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify', methods=['POST'])
def verify():
    username = request.form['username']
    
    # Fetch user ID from Roblox API
    user_id = fetch_user_id(username)
    
    if user_id:
        # Generate a verification token (you can use a more secure method)
        verification_token = 'andinewfiuneyarisbnyfiwnfyewnqrfijasndiddufnewuifnuaewifnyu4ewia'  # Change this to a secure method
        
        # Send verification token to user's Roblox account (simulate here)
        send_verification_to_roblox(username, verification_token)
        
        # Render the verify template with username and token
        return render_template('verify.html', username=username, token=verification_token)
    else:
        flash('User not found or banned. Please enter a valid Roblox username.', 'error')
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


def send_verification_to_roblox(username, token):
    # Simulate sending token to user's Roblox account (replace with actual implementation)
    print(f'Sending verification token {token} to {username}')


if __name__ == '__main__':
    app.run(debug=True)
