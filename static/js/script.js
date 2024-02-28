document.addEventListener("DOMContentLoaded", function () {
    const exit_button = document.getElementById("exit")
    const play_button = document.getElementById("play")

    // Opening login modal on page load
    openLoginModal();

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
    
})

// functions for a login window
// When executed scroll will be disabled and enabled
function openLoginModal() { 
    document.getElementById("login-modal").style.display = "block";
    document.body.classList.add('disable-scroll');
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none";
    document.body.classList.remove('disable-scroll');
}