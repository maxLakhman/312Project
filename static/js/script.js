document.addEventListener("DOMContentLoaded", function () {

    const register_button = document.getElementById("register_submit");
    const login_button = document.getElementById("login_submit");

    // Lobby Redirect (brings up the interactive blackjack tables)
    play_button.addEventListener("click", function (event) {
        window.location.href = "/lobby";
    });

    // Login Submit Button
 
    // Handle login submission
    login_button.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form submission

        // Get input values
        const username = document.getElementById("login_username").value;
        const password = document.getElementById("login_password").value;

        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                const response = JSON.parse(this.responseText);
                if (response["status"] === "error") {
                    document.getElementById("login_success").innerText = "";
                    document.getElementById("login_error").innerText = response["message"];
                } else {
                    document.getElementById("login_error").innerText = "";
                    document.getElementById("login_success").innerText = response["message"];
                    window.location.reload(); // Reload the page on successful login
                }
            }
        };

        request.open("POST", "/auth");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"username": username, "password": password}));
    });

    // Handle registration submission
    register_button.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form submission

        // Get input values
        const username = document.getElementById("register_username").value;
        const password = document.getElementById("register_password").value;
        const password_confirm = document.getElementById("register_password_confirm").value;

        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                const response = JSON.parse(this.responseText);
                if (response["status"] === "error") {
                    document.getElementById("register_success").innerText = "";
                    document.getElementById("register_error").innerText = response["message"];
                } else {
                    // document.getElementById("register_error").innerText = "";
                    // document.getElementById("register_success").innerText = response["message"];
                    // window.location.reload(); // Reload the page on successful registration
                    document.getElementById("register_error").innerText = "";
                    document.getElementById("register_success").innerText = response["message"];
                    //Clear form fields after successful registration
                    document.getElementById("register_username").value = '';
                    document.getElementById("register_password").value = '';
                    document.getElementById("register_password_confirm").value = '';
                    // Removed window.location.reload() to prevent UI change to logged-in state
                }
            }
        };

        request.open("POST", "/register");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"username": username, "password": password, "password_confirm": password_confirm}));
    });
});

// Functions for login & register window manipulation
function openLoginModal() { 
    document.getElementById("login-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
    document.getElementById("login_success").innerText = "";
    document.getElementById("login_error").innerText = "";
}

function openRegisterModal(){
    document.getElementById("register-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeRegisterModal() {
    document.getElementById("register-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
    document.getElementById("register_success").innerText = "";
    document.getElementById("register_error").innerText = "";
}
