function changeBackgroundColor() {
    var color = prompt("Enter a color (e.g., 'red', '#00FF00', 'rgb(0, 0, 255)'): ");
    if (color) {
        localStorage.setItem('backgroundColor', color); // Store color in local storage
        document.body.style.backgroundColor = color; // Set the background color
    }
}

document.getElementById('change-background-btn').addEventListener('click', changeBackgroundColor);

window.addEventListener('load', function() {
    var storedColor = localStorage.getItem('backgroundColor');
    if (storedColor) {
        document.body.style.backgroundColor = storedColor; // Apply stored color on page load
    }
});

function redirectToSettings(){
    window.location.href = '/settings.html'
}

function redirectToHome(){
    window.location.href = '/'
}