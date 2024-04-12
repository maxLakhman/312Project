document.addEventListener('DOMContentLoaded', function() {
    // Change background color based on stored value
    var storedColor = localStorage.getItem('backgroundColor');
    if (storedColor) {
        document.body.style.backgroundColor = storedColor;
    }

    // Event listener for changing background color
    var changeBackgroundBtn = document.getElementById('change-background-btn');
    if (changeBackgroundBtn) {
        changeBackgroundBtn.addEventListener('click', function() {
            var color = prompt("Enter a color (e.g., 'red', '#00FF00', 'rgb(0, 0, 255)'): ");
            if (color) {
                localStorage.setItem('backgroundColor', color); // Store color in local storage
                document.body.style.backgroundColor = color; // Set the background color
            }
        });
    }
});

function redirectToSettings(){
    window.location.href = '/settings.html'
}

function redirectToHome(){
    window.location.href = '/'
}

document.addEventListener('DOMContentLoaded', function() {
    var audio = document.getElementById('audio-player');
    var playPauseButton = document.querySelector('#music-player button');

    // Load the saved state
    //var savedVolume = localStorage.getItem('playerVolume');
    //if(savedVolume !== null) {
    //    audio.volume = savedVolume;
    //    document.getElementById('volumeControl').value = savedVolume;
    //}

    var savedTime = localStorage.getItem('playerTime');
    if(savedTime !== null) {
        audio.currentTime = savedTime;
    }

    var isPlaying = localStorage.getItem('isPlaying');
    if(isPlaying === 'true') {
        audio.play();
        playPauseButton.textContent = 'Pause';
    }

    window.togglePlayPause = function() {
        if (audio.paused) {
            audio.play();
            playPauseButton.textContent = 'Pause';
            localStorage.setItem('isPlaying', 'true');
        } else {
            audio.pause();
            playPauseButton.textContent = 'Play';
            localStorage.setItem('isPlaying', 'false');
        }
    };

    //window.setVolume = function(value) {
     //   audio.volume = value;
     //   localStorage.setItem('playerVolume', value);
    //};

    // Save current time periodically
    audio.addEventListener('timeupdate', function() {
        localStorage.setItem('playerTime', audio.currentTime);
    });
});