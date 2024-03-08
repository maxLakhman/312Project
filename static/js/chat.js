window.onload = function() {
    initiateChatBoxes();
};

function sendChat(el) {
    let input = el.parentElement.getElementsByTagName("input")[0];

    var request = new XMLHttpRequest();

    request.onreadystatechange = function(){
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    console.log(response);
                    input.value = "";
                    loadMessages(el.parentElement.parentElement);
                } catch (error) {
                    console.error("Error parsing JSON response: ", error);
                }
            } else {
                console.error("Request failed with status: ", this.status);
            }
        }
    };
    
    // Making request
    request.open("POST", "/chat-messages");
    request.setRequestHeader("Content-Type", "application/json");

    // Filling data
    let username = "guest";
    let data = {"username": username, "message": input.value, "chat_box": el.parentElement.parentElement.id}
    
    // Sending to /register
    request.send(JSON.stringify(data));
}

function loadMessages(el) {
    var request = new XMLHttpRequest();

    request.onreadystatechange = function(){
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    console.log(response);
                    
                    let messageBox = el.getElementsByClassName("chat-message-container")[0];
                    loadHtmlMessages(response, messageBox)
                } catch (error) {
                    console.error("Error parsing JSON response: ", error);
                }
            } else {
                console.error("Request failed with status: ", this.status);
            }
        }
    };
    
    // Making request
    let url = `/chat-messages?chat_box=${encodeURIComponent(el.id)}`;
    request.open("GET", url);
    request.setRequestHeader("Content-Type", "application/json");

    // Sending request
    request.send();
}

function initiateChatBoxes() {
    let rooms = document.getElementsByClassName("chat-box");
    Array.from(rooms).forEach(element => {
        loadMessages(element);
    });
}

function loadHtmlMessages(messages, messageBox) {
    messageBox.innerHTML = '';

    messages = JSON.parse(messages);
    console.log(typeof messages);
    messages.forEach(message => {
        let messageElement = document.createElement('div');
        messageElement.classList.add('message');

        let text = document.createElement('p');
        text.textContent = message.message;

        // Create a span element for username
        const usernameElement = document.createElement('span');
        usernameElement.textContent = message.username + ": ";
        usernameElement.classList.add('username');

        text.insertBefore(usernameElement, text.firstChild);
        messageElement.appendChild(text);

        messageBox.appendChild(messageElement);
    });
}
