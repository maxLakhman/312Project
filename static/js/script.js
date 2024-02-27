document.addEventListener("DOMContentLoaded", function () {
console.log("penis")
    
    const exit_button = document.getElementById("exit")
    const play_button = document.getElementById("play")

    // Can only redirect to blank page.
    exit_button.addEventListener("click", function (event) {
        if (event.target === exit_button) {
            new_window = window.open("about:blank", "_self");
        }
    });

    // ToDo
    play_button.addEventListener("click", function (event) {
        if (event.target === play_button) {
            console.log("To do");
        }
    });
    
})