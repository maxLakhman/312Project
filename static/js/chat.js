window.onload = function() {
    
    initiateChatBoxes();

    // Updates every second 3 seconds
    // Turn off if you want to debug
    setInterval(() => {
        initiateChatBoxes();
    }, 200000)
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
    
    // Sending to /chat-messages
    request.send(JSON.stringify(data));
}

// Go through all the chat boxes and initiate all their data
function initiateChatBoxes() {
    let rooms = document.getElementsByClassName("chat-box");
    Array.from(rooms).forEach(element => {
        loadMessages(element);
    });
}

// Load the messages from the backend
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

// Load in the visual html
function loadHtmlMessages(messages, messageBox) {
    messageBox.innerHTML = '';

    messages = JSON.parse(messages);
    messages.forEach(message => {
        let messageElement = document.createElement('div');
        messageElement.classList.add('message');

        let text = document.createElement('p');
        text.textContent = message.message;

        // Create a span element for username
        const usernameElement = document.createElement('span');
        usernameElement.textContent = message.username + ": ";
        usernameElement.classList.add('username');

        // Create the like button
        const likeBtn = document.createElement('a');
        likeBtn.addEventListener('click', () => {
            likeMessage(message._id.$oid);
        })

        // Deal with coloring in the like button here

        // Heart
        likeBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" viewBox="0 0 24 18" fill="none" class="like-btn">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 6.00019C10.2006 3.90317 7.19377 3.2551 4.93923 5.17534C2.68468 7.09558 2.36727 10.3061 4.13778 12.5772C5.60984 14.4654 10.0648 18.4479 11.5249 19.7369C11.6882 19.8811 11.7699 19.9532 11.8652 19.9815C11.9483 20.0062 12.0393 20.0062 12.1225 19.9815C12.2178 19.9532 12.2994 19.8811 12.4628 19.7369C13.9229 18.4479 18.3778 14.4654 19.8499 12.5772C21.6204 10.3061 21.3417 7.07538 19.0484 5.17534C16.7551 3.2753 13.7994 3.90317 12 6.00019Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style=""/>
        </svg>
        `

        // Create like count
        const likeCount = document.createElement('p');
        likeCount.text = message.liked_list ? message.liked_list.length : 4;

        text.insertBefore(usernameElement, text.firstChild);
        text.append(likeBtn);
        text.append(likeCount);
        messageElement.appendChild(text);

        messageBox.appendChild(messageElement);
    });
}

// Send a request given an id to /like-message
function likeMessage(id) {
    var request = new XMLHttpRequest();

    request.onreadystatechange = function(){
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    console.log(response);

                    // toDo
                } catch (error) {
                    console.error("Error parsing JSON response: ", error);
                }
            } else {
                console.error("Request failed with status: ", this.status);
            }
        }
    };
    
    // Making request
    request.open("POST", "/like-message");
    request.setRequestHeader("Content-Type", "application/json");

    let data = {"id": id}
    
    // Sending to /like-message
    request.send(JSON.stringify(data));
}
