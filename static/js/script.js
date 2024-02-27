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
function openLoginModal() { 
    document.getElementById("loginModal").style.display = "block";
}

function closeLoginModal() {
    document.getElementById("loginModal").style.display = "none";
}