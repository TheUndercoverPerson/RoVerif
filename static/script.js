$(document).ready(function() {
    $('#usernameForm').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();
        $.ajax({
            type: 'POST',
            url: '/generate',
            data: {username: username},
            success: function(response) {
                $('#generatedString').val(response.random_string);
                $('#result').show();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#copyBtn').click(function() {
        var copyText = document.getElementById("generatedString");
        copyText.select();
        copyText.setSelectionRange(0, 99999); /* For mobile devices */
        document.execCommand("copy");
        alert("Copied the text: " + copyText.value);
    });

    $('#verifyBtn').click(function() {
        var username = $('#username').val();
        var robloxUsername = $('#robloxUsername').val();
        $.ajax({
            type: 'POST',
            url: '/verify',
            data: {username: username, roblox_username: robloxUsername},
            success: function(response) {
                if (response.success) {
                    $('#verifyResult').text('Success! The string was found in your Roblox profile description.');
                } else {
                    $('#verifyResult').text('The string was not found in your Roblox profile description.');
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
