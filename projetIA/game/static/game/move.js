window.onload = function() {
  document.getElementById("bdown").addEventListener("click", () => {
      main([1,0]); //l'axe X et l'axe Y sont inversés car génération de table selon un tableau à 2d
  });
  document.getElementById("bleft").addEventListener("click", () => {
    main([0,-1]);
  });
  document.getElementById("bright").addEventListener("click", () => {
    main([0,1]);
  });
  document.getElementById("bup").addEventListener("click", () => {
    main([-1,0]);
  });    
  this.updateBoard(board, pos);
}
async function main(movement) {
const response = await jsonRPC("/game/move", {game_id: game_id, player_id: curr_player, move: movement});
let pos = [];
for(player of response.players){
  pos[pos.length] = player.position;
}
if(response.code == 0){
  document.getElementById("errors").textContent= "";
  curr_player = response.current_player
  updateBoard(response.board, pos);
}
else if (response.code == 1){
  document.getElementById("errors").textContent= "Out of board action, try another move";
}
else if (response.code == 2){
  document.getElementById("errors").textContent= "You cannot go on an enemy cell, try another move";
}
printPlayerToPlay(response.players, curr_player);
if (response.winner != undefined){
  if(response.winner.tie){
    document.getElementById("wrapper").textContent= "";
    document.getElementById("player_to_play").textContent= "It's a tie with an amount of "+response.winner.nb_cell+" cells";
  }
  else{
    document.getElementById("wrapper").textContent= "";
    document.getElementById("player_to_play").textContent= "End of the game, the winner is: "+response.winner.name+" with an amount of "+response.winner.nb_cell+" cells";
  }
}
}

function updateBoard(boardContent, pos){

let table = document.querySelector("table");
table.textContent="";
generateTable(table, boardContent, pos);
}

function generateTable(table, data, pos) {
for (let element of data) {
  let row = table.insertRow();
  for (key in element) {
    let cell = row.insertCell();

    if(element[key] == 1){
      cell.className = colors[0];
    }
    else if (element[key] == 2){
      cell.className = colors[1];
    }
    else{
      cell.className="couleur3"
    }  
  }
}
for (let position in pos){

  let posX = pos[position][0]
  let posY = pos[position][1]
  let ligne1 = table.getElementsByTagName('tr')[posX];
  let cell1 = ligne1.getElementsByTagName('td')[posY];

  cell1.textContent= "P"+position 
}
}


function jsonRPC(url, data) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-type", "application/json");
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]")
      .value;
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject({
          status: this.status,
          statusText: xhr.statusText,
        });
      }
    };
    xhr.onerror = function () {
      reject({
        status: this.status,
        statusText: xhr.statusText,
      });
    };
    xhr.send(JSON.stringify(data));
  });
}


function printPlayerToPlay(players, indice){
for(let player of players){
  if(player.id == indice){
    document.getElementById("player_to_play").textContent= "P"+players.indexOf(player)+" to play";
  }
}
}