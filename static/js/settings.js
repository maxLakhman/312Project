document.addEventListener('DOMContentLoaded', function() {
    // Change background color based on stored value
    var storedColor = localStorage.getItem('backgroundColor');
    if (storedColor) {
        document.body.style.backgroundColor = storedColor;
    }

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

    var audio = document.getElementById('audio-player');

    // Load the saved state
    var savedVolume = localStorage.getItem('playerVolume');
    if(savedVolume !== null) {
        audio.volume = savedVolume;
        //document.getElementById('volumeControl').value = savedVolume;
    }
    var savedTime = localStorage.getItem('playerTime');
    if(savedTime !== null) {
        audio.currentTime = savedTime;
    }
    var isPlaying = localStorage.getItem('isPlaying');
    if(isPlaying === 'true') {
        console.log("after lookup state, game plays")
        audio.play();
    }else{
        console.log("after lookup state, game pause")
        audio.pause();
    }

    //Event listeners here
    // Add event listener for 'play' event
    audio.addEventListener('play', function() {
        console.log('Audio playback started');
        localStorage.setItem('isPlaying', 'true');
        // You can add your custom logic here
    });

    // Add event listener for 'pause' event
    audio.addEventListener('pause', function() {
        console.log('Audio playback paused');
        localStorage.setItem('isPlaying', 'false');
        // You can add your custom logic here
    });
    // Add event listener for 'volumechange' event
    audio.addEventListener('volumechange', function() {
        var volume = audio.volume;
        console.log('Volume changed:', volume);
        localStorage.setItem('playerVolume', volume);
    });

    // Save current time periodically
    audio.addEventListener('timeupdate', function() {
        localStorage.setItem('playerTime', audio.currentTime);
    });
});

function redirectToSettings(){
    window.location.href = '/settings.html'
}

function redirectToHome(){
    window.location.href = '/'
}