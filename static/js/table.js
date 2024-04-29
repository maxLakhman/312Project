
// Onload init game
window.onload = function() {
    init_game();
};


// sending the socket request for a first hand whenever a user joins the page
function init_game(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('init_game', {"table_id": table_id});
}

socket.on('init_players', function(data){
    if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        let game_starting = document.getElementById("game_starting");
        game_starting.innerText = data.message;
        game_starting.style.display = "block";

        if(data.message === "Game starting..."){
            setTimeout(function(){
                game_starting.innerText = "";
                game_starting.style.display = "none";
            }, 2000);
        }
    }
});


socket.on('current_player', function(data){
    if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        let username = data.username;
        let time_remaining = data.time;
        let game_starting = document.getElementById("game_starting");
        if(time_remaining === 0){
            game_starting.innerText = `${username} has folded.`;
        }
        else{
            game_starting.innerText = `${username}\'s turn. They have ${time_remaining} seconds to move or they will fold.`;
            game_starting.style.display = "block";
        }


    }
});

function hit(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('hit', {"table_id":table_id});
}
function stand(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('stand', {"table_id":table_id});
}

function fold(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('fold', {"table_id":table_id});
}

socket.on('new_turn', function(data){
    if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        console.log(data.username);
    }
});

function display_hand(data){
    if(data.dealer_hand){
        var dealer_hand = data.dealer_hand;
        var dealer_id = 'dealer-hand';
        var dealer_hand_elem = document.getElementById(dealer_id);
        dealer_hand_elem.innerHTML = '';
        for (var i = 0; i < dealer_hand.length; i++){
            var img = document.createElement('img');
            img.src = '/static/images/cards2/' + dealer_hand[i] + '.png';
            img.className = 'card';
            img.alt = dealer_hand[i];
            img.style.width = '100px';
            img.style.height = 'auto';
            dealer_hand_elem.appendChild(img);
        }
        dealer_hand_elem.style.display = 'flex';
        dealer_hand_elem.style.flexDirection = 'row';
    }
    else{
        var player_hand = data.player_hand;
        var player_name = data.username;
        var element_id = 'hand-' + player_name;
        
        // find the elements
        var player_box = document.getElementById('player_box');
        var hand = document.getElementById(element_id);
        hand.innerHTML = '';
    
        // set the images
        for (var i = 0; i < player_hand.length; i++){
            var img = document.createElement('img');
            img.src = '/static/images/cards2/' + player_hand[i] + '.png';
            img.className = 'card';
            img.alt = player_hand[i];
            img.style.width = '100px';
            img.style.height = 'auto';
            hand.appendChild(img);
        }
    
    }
    hand.style.display = 'flex';
    hand.style.flexDirection = 'row';
    
}

// receiving hand data from the server
socket.on('update_hand', function(data){
        console.log(data);
        // creating the table
        display_hand(data);
});
