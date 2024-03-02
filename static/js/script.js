document.addEventListener("DOMContentLoaded", function () {
    // Action Elements
    const exit_button = document.getElementById("exit")
    const play_button = document.getElementById("play")
    const register_button = document.getElementById("register_submit")
    const login_button = document.getElementById("login_submit")
    // Opening login modal on page load
    // openLoginModal();

    // Can only redirect to blank page.
    exit_button.addEventListener("click", function (event) {
        if (event.target === exit_button) {
            new_window = window.open("https://www.google.com/", "_self");
        }
    });

    // ToDo
    play_button.addEventListener("click", function (event) {
        if (event.target === play_button) {
            console.log("To do");
        }
    });

    // Login Submit Button
    login_button.addEventListener("click", function (event) {
        // Stopping default close on click
        event.preventDefault();

        // Getting Fields
        const username = document.getElementById("login_username").value;
        const password = document.getElementById("login_password").value;
        console.log("Username: " + username);
        console.log("Password: " + password);

    });
    
    // Register Submit Button
    register_button.addEventListener("click", function (event) {

        // Stopping default close on submit
        event.preventDefault();

        // Getting Text Fields
        const username = document.getElementById("register_username").value
        const password = document.getElementById("register_password").value
        const password_confirm = document.getElementById("register_password_confirm").value

        // Creating new request
        var request = new XMLHttpRequest();

        request.onreadystatechange = function(){
            if(this.readyState ===4 && this.status === 200){

                // Getting response from app.py def register()
                const response = JSON.parse(this.responseText);
        

                // Setting error message
                if(response["status"] === "error"){
                    document.getElementById("register_success").innerText = "";
                    document.getElementById("register_error").innerText = response["message"];
                }
                // Setting success message
                else{
                    document.getElementById("register_error").innerText = "";
                    document.getElementById("register_success").innerText = response["message"];

                    // Closing register window after 3 sec
                    setTimeout(function() {
                        closeRegisterModal();
                    }, 3000);
                }
            }
        };

        request.open("POST", "/register");
        request.setRequestHeader("Content-Type", "application/json");

        // Filling data
        let data = {"username": username, "password": password, "password_confirm": password_confirm}
        
        // Sending to /register
        request.send(JSON.stringify(data));
    });
})

// functions for a login & register window
// When executed scroll will be disabled and enabled
function openLoginModal() { 
    document.getElementById("login-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
}

function openRegisterModal(){
    document.getElementById("register-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeRegisterModal() {
    document.getElementById("register-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
}

