// save the tables on load
var tables = [];



// function to create a new table
function createTable() {
    // send a request to create a new table
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState ===4 && this.status === 200){
            const response = JSON.parse(this.responseText);
            if(response.status === "success") {
                window.location.href = response.redirect;
            }
            else{}
        }
    };

    // making the request
    request.open("POST", "/create-table");
    
    // sending the request
    request.send();
}

// function to join a table
function joinTable(table_id){
    console.log(table_id);
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState ===4 && this.status === 200){
            window.location.href = "/join-table/" + table_id;
        }
    };

    // making the request
    request.open("GET", ("/join-table/" + table_id));

    // sending the request
    request.send(JSON.stringify({"table_id": table_id}));
    
}
