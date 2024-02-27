document.addEventListener("DOMContentLoaded", function () {
    console.log("penis");
    
    // const exit_button = document.getElementById("exit")
    const play_button = document.getElementById("play")

    play_button.addEventListener("click", function (event) {
        if (event.target === play_button) {
            console.log("To do");
        }
    });
    
})