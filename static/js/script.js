document.addEventListener("DOMContentLoaded", function () {
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
        // Stopping default close
        event.preventDefault();

        // Getting Fields
        const username = document.getElementById("login_username").value;
        const password = document.getElementById("login_password").value;
        console.log("Username: " + username);
        console.log("Password: " + password);

        // ToDo: Get username from database
        if(username === "penis"){

        }
        else{
            document.getElementById("login_error").innerText = "Invalid Username";
        }

        // ToDo: Get password from database
        if(password === "poop"){

        }
        else{
            document.getElementById("login_error").innerText = "Invalid Password";
        }


    });
    
    // Register Submit Button
    register_button.addEventListener("click", function (event) {
        // Stopping default close
        event.preventDefault();

        // Getting fields
        const username = document.getElementById("register_username").value;
        const password = document.getElementById("register_password").value;
        const password_confirm = document.getElementById("register_password_confirm").value;

        // Check if fields are empty
        if(!username || !password || !password_confirm){
            document.getElementById("register_error").innerText = "All Fields Must Be Filled"
        }
        // ToDo: Check database if username is taken
        else if (username === "penis"){

        }
        // Check for password missmatch
        else if(password !== password_confirm){
            document.getElementById("register_error").innerText = "Passwords Do Not Match";
        }
        // Todo: Register user
        else {
            
        }

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

