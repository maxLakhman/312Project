

// sending the socket request for a first hand whenever a user joins the page
function first_hand(){
    socket.emit('first_hand');

    // receiving the first hand from the server
    socket.on('hand', function(data){
        console.log(data);
        // creating the table
        display_hand(data);
    });

}

function hit(){
    socket.emit('hit');

    // receiving the hand from the server
    socket.on('hand', function(data){
        console.log(data);
        display_hand(data);
    });
}

function display_hand(data){
    // find the player hand
    var player_hand = data.hand;
    var player_name = data.usernname;
    
    // find the elements
    var player_box = document.getElementById('player_box');
    var hand = document.getElementById('hand-' + player_name);

    // set the images
    for (var i = 0; i < player_hand.length; i++){
        var img = document.createElement('img');
        img.src = '/static/images/cards2/' + player_hand[i] + '.png';
        img.className = 'card';
        hand.appendChild(img);
    }
}
