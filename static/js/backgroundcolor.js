// Get the modal
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("open-model-btn");
    var span = document.getElementsByClassName("close")[0];
    var dark = document.getElementById("dark");
    var light = document.getElementById("light");

    if (dark != null){
        dark.onclick = function () {
                    console.log("dark clicked")
                    localStorage.setItem('backgroundcolor', 'black');
                    document.body.style.backgroundColor = "black";
            }

            light.onclick = function () {
                console.log("light clicked")
                localStorage.setItem('backgroundcolor', 'white');
                document.body.style.backgroundColor = "white";
            }

            // When the user clicks the button, open the modal
            btn.onclick = function() {
                console.log("btn clicked");
                modal.style.display = "block";
            }

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
    }


document.addEventListener('DOMContentLoaded', function() {
    color = localStorage.getItem('backgroundcolor');
    if (color){
        document.body.style.backgroundColor = color;
    }
});