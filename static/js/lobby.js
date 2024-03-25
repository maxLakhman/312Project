// save the tables on load
var tables = [];



// function to create a new table
function createTable() {
    // send a request to create a new table
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState ===4 && this.status === 200){
            const response = JSON.parse(this.responseText);
            if(response["status"] === "error"){
                document.getElementById("table_error").innerText = response["message"];
            }
            else{
                window.location.href = "/join-table/" + response["table_id"];
            }
        }
    };

    // making the request
    request.open("POST", "/create-table");
    
    // sending the request
    request.send();
}

// function to join a table
function joinTable(table_id){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState ===4 && this.status === 200){
            const response = JSON.parse(this.responseText);
            if(response["status"] === "error"){
                document.getElementById("table_error").innerText = response["message"];
            }
            else{
                window.location.href = "/join-table/" + table_id;
            }
        }
    };
}

// function to add the tables to the lobby gallery
function addTables(tables){
    const gallery = document.getElementById("table-gallery");
    gallery.innerHTML = "";
    for (const table of tables){
        const table_div = document.createElement("div");
        table_div.className = "table";
        table_div.innerHTML = table["name"];
        table_div.addEventListener("click", function(){
            joinTable(table["id"]);
        });
        gallery.appendChild(table_div);
    }
}