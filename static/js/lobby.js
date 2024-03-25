
// function to create a new table
function createTable() {
    
    // send a request to create a new table
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState ===4 && this.status === 200){
            const response = JSON.parse(this.responseText);
            if(response["status"] === "error"){
            }
            else{
                window.location.href = "/table/" + response["table_id"];
            }
        }
    };
}