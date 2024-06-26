users = [];

// Onload init game
window.onload = function() {
    init_game();
    socket.emit('user_connect', {"username": getUsername()});
};


// sending the socket request for a first hand whenever a user joins the page
function init_game(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('init_game', {"table_id": table_id});
}

socket.on('user_connected', function(data){
    let username = data.username;
    let table_id = data.table_id["table"];

    if(table_id == document.getElementById("table_id").getAttribute("data-id")) {

        if(!users.includes(username) && username != getUsername()) {
            users.push(username);

            createUserElement(username);
        }
    }
});

socket.on('user_disconnected', function(data){
    let username = data.username;
    let table_id = data.table_id["table"];

    if(table_id == document.getElementById("table_id").getAttribute("data-id")) {

        if(users.includes(username) && username != getUsername()) {
            users.del(username);

            let index = users.indexOf(username);

            if (index !== -1) {
                users.splice(index, 1);
            }

            var playerElement = document.getElementById("player-" + username);

            if (playerElement) {
                playerElement.remove();
            }
        }
    }
});

function createUserElement(username) {
    const players_container = document.getElementById("player-box");

    let player = document.createElement("div");
    player.classList.add("player");
    player.id = "player-" + username;

    let player_header = document.createElement("h2");
    player_header.innerText = username;

    let balance = document.createElement("p");
    balance.innerText = "Balance: 0";

    let bet = document.createElement("p");
    balance.innerText = "Bet: 0";

    let hand = document.createElement("p");
    hand.id = "value-elm-" + username;
    hand.innerText = "Hand: 0";

    let hand_div = document.createElement("div");
    hand_div.classList.add("hand");
    hand_div.id = "hand-" + username;
    
    player.appendChild(player_header);
    player.appendChild(balance);
    player.appendChild(bet);
    player.appendChild(hand);
    player.appendChild(hand_div);

    players_container.appendChild(player);
}

socket.on('game_over', function(data){
    if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        let container = document.getElementById("outcome");
        document.getElementById("end-game-modal").style.display = "block";
        let header = document.getElementById("end-game-header-text");
        let current_user = getUsername();
        let outcome = data.outcome

        // loop through players
        for(let player in outcome){
            let player_info = outcome[player];

            let value = player_info.value;
            let message = player_info.message;
            let hand = player_info.hand;
            let bet = player_info.bet;
            let total = player_info.total;

            if(message === "won"){
                bet *= 2;
            }


            if(player === current_user){
                let text = document.getElementById("end-game-header-text")
                if(message === "tied"){
                    text.innerText = `You ${message}! Your bet of ${bet} tokens has been returned to you.`;
                }
                else{
                    text.innerText = `You ${message} ${bet} tokens! You have a total of ${total} tokens.`;
                }
            }
            else{
                let span = document.createElement("span");
                if(message === "tied"){
                    span.textContent = `${player} ${message}! Their bet of ${bet} tokens has been returned.`;
                }
                else{
                    span.textContent = `${player} ${message} ${bet} tokens! They have a total of ${total} tokens.`;
                }
                span.className += " player-result";
                let text_container = document.getElementById("end-game-text")
                text_container.appendChild(span);
                text_container.appendChild(document.createElement("br"));
            }
        }
    }
});

socket.on('init_players', function(data){
    if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        let game_starting = document.getElementById("game_starting");
        game_starting.innerText = data.message;
        game_starting.style.display = "block";

        if(data.message === "Game starting..."){
            setTimeout(function(){
                player_ready_btn = document.getElementById("start_now_btn");
                player_ready_btn.style.display = "none";
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

function increaseBet(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('increase_bet', {"table_id":table_id});
}

function decreaseBet(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit('decrease_bet', {"table_id":table_id});
}

socket.on('update_bet', function(data){
    console.log(data);
    console.log(users);


    let username = data.username;
    let bet = data.bet;
    let balance = data.balance;

    let user_div = document.getElementById("player-" + username);

    let bet_elem = user_div.getElementsByTagName("p")[1];
    bet_elem.innerText = `Bet: ${bet}`;
    
    let balance_elem = user_div.getElementsByTagName("p")[0];
    balance_elem.innerText = `Balance: ${balance}`;
    
    
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
    if(data.dealer_hand && data.table_id == document.getElementById("table_id").getAttribute("data-id")){
        var dealer_hand = data.dealer_hand;
        var dealer_id = 'dealer-hand';
        var dealer_hand_elem = document.getElementById(dealer_id);
        dealer_hand_elem.innerHTML = '';
        
        if(data.is_end == true) {
            let value_elm = document.getElementById("dealer-hand-value");
            value_elm.innerText = "Hand: " + data.value;
        }

        let loopLength = (dealer_hand.length == 2 && data.is_end == false) ? 1 : dealer_hand.length;

        for (var i = 0; i < loopLength; i++){
            var img = document.createElement('img');
            img.src = '/static/images/cards2/' + dealer_hand[i] + '.png';
            img.className = 'card';
            img.alt = dealer_hand[i];
            img.style.width = '100px';
            img.style.height = 'auto';
            dealer_hand_elem.appendChild(img);
        }

        if (dealer_hand.length == 2 && data.is_end == false) {
            var img = document.createElement('img');
            img.src = '/static/images/cards2/back.png';
            img.className = 'card';
            img.alt = dealer_hand[i];
            img.style.width = '100px';
            img.style.height = 'auto';
            dealer_hand_elem.appendChild(img);
        }

        dealer_hand_elem.style.display = 'flex';
        dealer_hand_elem.style.flexDirection = 'row';
    }
    else if(data.table_id == document.getElementById("table_id").getAttribute("data-id")) {
        var player_hand = data.player_hand;
        var player_name = data.username;
        var element_id = 'hand-' + player_name;
        
        // find the elements
        var player_box = document.getElementById('player_box');
        var hand = document.getElementById(element_id);
        hand.innerHTML = '';

        try {
            let value_elm = document.getElementById("value-elm-" + data.username);
            value_elm.innerText = "Hand: " + data.value;
        } catch {}
    
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
    
}

// receiving hand data from the server
socket.on('update_hand', function(data){
        console.log(data);
        // creating the table
        display_hand(data);
});

function start_now(){
    let table_id = document.getElementById("table_id").getAttribute("data-id");
    socket.emit("player_ready", {"table_id":table_id});
}

function closeEndGameModal(){
    window.location.href = '/';
}