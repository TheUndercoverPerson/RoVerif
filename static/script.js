$(document).ready(function() {
    // Handle form submission to generate random string
    $('#usernameForm').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();

        $.ajax({
            type: 'POST',
            url: '/generate',
            data: { username: username },
            success: function(response) {
                $('#generatedString').val(response.random_string);
                $('#result').show();
            }
        });
    });

    // Handle click event for "Search Profile" button
    $('#searchProfileBtn').click(function() {
        var username = $('#username').val();
        var generatedString = $('#generatedString').val();

        $.ajax({
            type: 'POST',
            url: '/verify',
            data: { username: username, roblox_username: generatedString }, // Sending generatedString as roblox_username
            success: function(response) {
                if (response.success) {
                    $('#verifyResult').text('String found in profile description! Success!');
                } else {
                    $('#verifyResult').text('String not found in profile description.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
