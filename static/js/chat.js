
function sendChat(el) {
    let input = el.parentElement.getElementsByTagName("input")[0];

    var request = new XMLHttpRequest();

    request.onreadystatechange = function(){
        // Getting response
        const response = JSON.parse(this.responseText);
        console.log(response)
    };
    
    // Making request
    request.open("POST", "/chat-messages");
    request.setRequestHeader("Content-Type", "application/json");

    // Filling data
    let data = {"username": "guest", "message": input.value, "chat_box": input.id}
    
    // Sending to /register
    request.send(JSON.stringify(data));
}