const axios = require('axios');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// Roblox API endpoints
const API_ENDPOINT = "https://users.roblox.com/v1/usernames/users";
const DESCRIPTION_ENDPOINT = "https://users.roblox.com/v1/users/";

// Home route
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// Verification route
app.post('/verify', async (req, res) => {
    const username = req.body.username;

    if (!username) {
        return res.status(400).send("Username is required.");
    }

    try {
        // Fetch user ID from Roblox API
        const userId = await fetchUserId(username);

        if (userId) {
            // Generate a random verification token
            const verificationToken = generateRandomToken();

            // Store the token, username, and user ID for verification
            req.session.verificationToken = verificationToken;
            req.session.username = username;
            req.session.userId = userId;

            // Debugging information
            console.log(`Debug Info: Username: ${username}, User ID: ${userId}, Verification Token: ${verificationToken}`);

            // Send verification token to client
            res.json({ token: verificationToken });
        } else {
            return res.status(404).send("User not found or banned. Please enter a valid Roblox username.");
        }
    } catch (error) {
        console.error(`Error: ${error.message}`);
        return res.status(500).send("Internal Server Error");
    }
});

// Check verification route
app.post('/check_verification', async (req, res) => {
    const storedToken = req.session.verificationToken;
    const username = req.session.username;
    const userId = req.session.userId;

    if (!storedToken || !username || !userId) {
        return res.status(400).send("Verification session expired. Please try again.");
    }

    try {
        // Fetch user profile description
        const description = await fetchProfileDescription(userId);

        // Debugging information
        console.log(`Debug Info: Stored Token: ${storedToken}, Description: ${description}, User ID: ${userId}`);

        if (description && description.includes(storedToken)) {
            return res.status(200).send(`Verification successful for user: ${username}`);
        } else {
            return res.status(403).send("Verification failed. Please ensure the token is added to your profile and try again.");
        }
    } catch (error) {
        console.error(`Error: ${error.message}`);
        return res.status(500).send("Internal Server Error");
    }
});

// Function to fetch user ID from Roblox API
async function fetchUserId(username) {
    try {
        const response = await axios.post(API_ENDPOINT, {
            usernames: [username],
            excludeBannedUsers: true
        });
        if (response.status === 200 && response.data.data.length > 0) {
            return response.data.data[0].id;
        } else {
            return null;
        }
    } catch (error) {
        throw new Error(`Failed to fetch user ID: ${error.message}`);
    }
}

// Function to fetch user profile description from Roblox API
async function fetchProfileDescription(userId) {
    try {
        const response = await axios.get(`${DESCRIPTION_ENDPOINT}${userId}`);
        if (response.status === 200 && response.data.description) {
            return response.data.description;
        } else {
            return "";
        }
    } catch (error) {
        throw new Error(`Failed to fetch profile description: ${error.message}`);
    }
}

// Function to generate random verification token
function generateRandomToken(length = 6) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let token = '';
    for (let i = 0; i < length; i++) {
        token += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return token;
}

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
