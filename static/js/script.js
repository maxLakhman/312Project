document.addEventListener("DOMContentLoaded", function () {
    // Action Elements
    
    const exit_button = document.getElementById("exit");
    const play_button = document.getElementById("play");
    const register_button = document.getElementById("register_submit");
    const login_button = document.getElementById("login_submit");
    const upload_button = document.getElementById("profile_pic_submit");
    const profile_pic = document.getElementById("user-profile-pic");
    // Opening login modal on page load
    // openLoginModal();

    // Lobby Redirect (brings up the interactive blackjack tables)
    play_button.addEventListener("click", function (event) {
        console.log(getUsername());
        if(getUsername() != "") {
            window.location.href = "/lobby";
        } else {
            openRegisterModal();
        }
    });

    document.getElementById("login-in-register").addEventListener("click", function() {
        closeRegisterModal();
        openLoginModal();
    });

    document.getElementById("register-in-login").addEventListener("click", function() {
        closeLoginModal();
        openRegisterModal();
    });

    // Login Submit Button
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
                    window.location.reload(); // Reload the page on successful registration
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

    // Profile Pic submission
// Profile Pic submission
    profile_pic.addEventListener("click", function(event){
        openUploadModal();
    });
    
    upload_button.addEventListener("click", function (event){
        event.preventDefault();
        var file = document.getElementById('profile_pic').files[0];
        var formData = new FormData();
        formData.append('profile_pic', file);

        var request = new XMLHttpRequest();
        request.open("POST", "/profile-pic");
        request.onreadystatechange = function() {
            if (request.readyState === 4){
                // Worked
                let error_text = document.getElementById("upload-error-msg");
                if(request.status === 200){
                    const response = JSON.parse(this.responseText);
                    console.log(response);
                    if (response['status'] === "success"){
                        document.getElementById("upload-error-msg").innerText = '';
                        document.getElementById("profile-pic-preview").src = "./"+ response["filepath"];
                        document.getElementById("user-profile-pic").src ="./"+ response["filepath"];
                    }
                }
                // Bad file type
                else if(request.status === 400){
                    json_response = JSON.parse(this.response);
                    error_text.innerText = json_response.message;
                }
                // Image too large
                else if (request.status === 413){
                    error_text.innerText = "Image size must be less than 1MB."
                }

            }
            // if (request.readyState === 4 && request.status === 200) {
                // const response = JSON.parse(this.responseText);
                // console.log(response);
                // if (response['status'] === "success"){
                //     document.getElementById("profile-pic-preview").src = "./"+ response["filepath"];
                //     document.getElementById("user-profile-pic").src ="./"+ response["filepath"];
                // }
            // }
            
        };
        request.send(formData); // Send the FormData object
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

function openUploadModal() {
    document.getElementById("update-profile-pic-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeUploadModal() {
    document.getElementById("upload-error-msg").innerText = '';
    document.getElementById("update-profile-pic-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
}
