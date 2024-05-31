const HIDDEN = "display:none;";
const SHOWN = "display:block;";
const PLAYER_1_LEFT = "A";
const PLAYER_1_RIGHT = 'S';
const PLAYER_1_MIDPOINT = 'D';
const PLAYER_1_TRAPEZOIDAL = 'F';
const PLAYER_2_LEFT = "J";
const PLAYER_2_RIGHT = "K";
const PLAYER_2_MIDPOINT = "L";
const PLAYER_2_TRAPEZOIDAL = ";";
const LEFT = 0;
const RIGHT = 1;
const MIDPOINT = 2;
const TRAPEZOIDAL = 3;
const BUTTONSTOANSWER = "<div id = 'answers'> <div id = 'player1'> <h3>Player 1: Answer Here</h3> <button onclick='processGameAnswer(1, 0)' id = 'oneleft'>Left Rienmann Sum</button> <button onclick = 'processGameAnswer(1, 1)' id = 'oneright'>Right Rienmann Sum</button><button onclick = 'processGameAnswer(1,2)' id = 'onemid'>Midpoint Rienmann Sum</button><button onclick = 'processGameAnswer(1,3)' id = 'onetrap'>Trapezoidal Rienmann Sum</button></div><div id = 'player2'><h3>Player 2: Answer Here</h3><button onclick='processGameAnswer(2, 0)' id = 'twoleft'>Left Rienmann Sum</button><button onclick = 'processGameAnswer(2, 1)' id = 'tworight'>Right Rienmann Sum</button><button onclick = 'processGameAnswer(2,2)' id = 'twomid'>Midpoint Rienmann Sum</button><button onclick = 'processGameAnswer(2,3)' id = 'twotrap'>Trapezoidal Rienmann Sum</button></div></div>"
var identify = Math.round((Math.random()*10000000))+2;
const MY_IDENTIFIER = identify;
console.log(MY_IDENTIFIER)
var theIndexToStartSplicing = 0;
function doSubmit() {
    var selectMe = document.getElementById('selectme');
    var inputTable = document.getElementById('theInputTable');
    var rienmannSelection = document.getElementById("theSelection");
    var sendDataButton = document.getElementById("sendDataButton");
    var playerNameTable = document.getElementById("getTheData");
    var startGameButton = document.getElementById("startGameButton");
    var submitButton = document.getElementById("submitOptions");
    var mainHeader = document.getElementById("headerMain");
    var calculatorRowAmountGetter = document.getElementById("getRowAmount");
    var value = selectMe.value;
    if (value == 0) {
        selectMe.style = HIDDEN;
        calculatorRowAmountGetter.style = SHOWN;
        submitButton.style = HIDDEN;
    }else if(value == 1)
    {
        selectMe.style = HIDDEN;
        submitButton.style = HIDDEN;
        playerNameTable.style = SHOWN;
        startGameButton.style = SHOWN;
    }
}
function calculatorStarterTwo(value)
{
    var selectMe = document.getElementById('selectme');
    var inputTable = document.getElementById('theInputTable');
    var rienmannSelection = document.getElementById("theSelection");
    var sendDataButton = document.getElementById("sendDataButton");
    var playerNameTable = document.getElementById("getTheData");
    var startGameButton = document.getElementById("startGameButton");
    var submitButton = document.getElementById("submitOptions");
    var mainHeader = document.getElementById("headerMain");
    var calculatorRowAmountGetter = document.getElementById("getRowAmount");
    createTable(parseInt(value));
    inputTable.style = SHOWN;
    rienmannSelection.style = SHOWN;
    sendDataButton.style = SHOWN;
    calculatorRowAmountGetter.style = HIDDEN;
    
    
}

function createTableRow(id1, id2) {
    var elementTr = document.createElement('tr');
    var template1 = document.createElement('td');
    var input1 = document.createElement('input');
    input1.type = 'number';
    input1.id = id1;
    input1.value = Math.round(Math.random() * 100);
    template1.appendChild(input1);
    elementTr.appendChild(template1);
    var template2 = document.createElement('td');
    var input2 = document.createElement('input');
    input2.type = 'number';
    input2.id = id2;
    input2.value = Math.round(Math.random() * 100);
    template2.appendChild(input2);
    elementTr.appendChild(template2);
    return elementTr;
}

function createTable(numElements) {
    for (var i = 1; i <= numElements; i++) {
        document.getElementById('theInputTable').appendChild(createTableRow('x' + i, 'y' + i));
    }
}

function sendData() {
    var table = document.getElementById('theInputTable');
    var inputs = table.getElementsByTagName('input');
    var whichRienmann = document.getElementById("theSelection");
    var data = {"identifier": MY_IDENTIFIER};

    for (var i = 0; i < inputs.length; i += 2) {
        var xValue = inputs[i].value;
        var yValue = inputs[i + 1].value;
        data['x' + (i / 2 + 1)] = xValue;
        data['y' + (i / 2 + 1)] = yValue;
    }
    data['rienmannSelection'] = whichRienmann.value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submit", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var element = document.getElementById('theBody');
            var bodyContent = element.innerHTML;
            console.log("BODY BEFORE MODS:"+bodyContent)
            console.log(bodyContent.indexOf("<div id"))
            bodyContent = bodyContent.substring(0, bodyContent.indexOf("<div id"));
            //xhr.responseText
            document.write(bodyContent);
            console.log("BODY"+bodyContent);
            document.write(BUTTONSTOANSWER);
            document.write("<div id = 'graph'>")
            document.write(xhr.responseText);
            document.write("</div>");
            var selectMe = document.getElementById('selectme');
    var inputTable = document.getElementById('theInputTable');
    var rienmannSelection = document.getElementById("theSelection");
    var sendDataButton = document.getElementById("sendDataButton");
    var playerNameTable = document.getElementById("getTheData");
    var startGameButton = document.getElementById("startGameButton");
    var submitButton = document.getElementById("submitOptions");
    var mainHeader = document.getElementById("headerMain");
    var calculatorRowAmountGetter = document.getElementById("getRowAmount");
    inputTable.style = HIDDEN;
    selectMe.style = SHOWN;
    submitButton.style = SHOWN;
    calculatorRowAmountGetter.style = HIDDEN;
    rienmannSelection.style = HIDDEN;
    sendDataButton.style = HIDDEN;

            
        }
    };
    xhr.send(JSON.stringify(data));
    
}

function startGame(event)
{
    event.preventDefault();
    console.log("Start game triggered")
    var name1Element = document.getElementById("player1Name"); //the element for name1
    var name2Element = document.getElementById("player2Name"); //the element for name2
    var selectMe = document.getElementById('selectme');
    var inputTable = document.getElementById('theInputTable');
    var rienmannSelection = document.getElementById("theSelection");
    var sendDataButton = document.getElementById("sendDataButton");
    var playerNameTable = document.getElementById("getTheData");
    var startGameButton = document.getElementById("startGameButton");
    var submitButton = document.getElementById("submitOptions");
    var mainHeader = document.getElementById("headerMain");
    var calculatorRowAmountGetter = document.getElementById("getRowAmount");
    var graph = document.getElementById("graph");
    console.log("Variables declared in startGame")
    
    graph.style = SHOWN;
    console.log("Graph style set")

    
    var name1 = name1Element.value;
    
    var name2 = name2Element.value;
    console.log("Name elements read")
    playerNameTable.style = HIDDEN;
    var data = {"identifier": MY_IDENTIFIER,"isGame": 'data', "name1":name1, "name2":name2};
    console.log("Data created")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submit");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var element = document.getElementById('theBody');
            console.log(name1+name2+xhr.responseText)
            var bodyContent = element.innerHTML;
            //console.log(bodyContent)
            
            bodyContent = bodyContent.substring(0, bodyContent.indexOf("<div id"));
            //xhr.responseText
            document.body.id = "theBody";
            document.write(bodyContent);
            //document.write("Player 1: Use A for left, S for right, D for midpoint, and F for trapezoidal.\n Player 2: Use ; for left, L for right, K for midpoint, and J for trapezoidal.");
            document.body.onkeydown = function(ev)
            {
                key = ev.key;
                var oneLeft = document.getElementById("oneleft");
                var twoLeft = document.getElementById("twoleft");
                var oneRight = document.getElementById("oneright");
                var twoRight = document.getElementById("tworight");
                var oneMidpoint = document.getElementById("onemid");
                var twoMidpoint = document.getElementById("twomid");
                var oneTrapezoidal = document.getElementById("onetrap");
                var twoTrapezoidal = document.getElementById("twotrap")
                console.log("Key pressed: "+key)
                switch(key.toUpperCase())
                {
                    case PLAYER_1_LEFT:
                        oneLeft.click();
                        break;
                    case PLAYER_2_LEFT:
                        twoLeft.click();
                        break;
                    case PLAYER_1_RIGHT:
                        oneRight.click();
                        break;
                    case PLAYER_2_RIGHT:
                        twoRight.click();
                        break;
                    case PLAYER_1_MIDPOINT:
                        oneMidpoint.click();
                        break;
                    case PLAYER_2_MIDPOINT:
                        twoMidpoint.click();
                        break;
                    case PLAYER_1_TRAPEZOIDAL:
                        oneTrapezoidal.click();
                        break;
                    case PLAYER_2_TRAPEZOIDAL:
                        twoTrapezoidal.click();
                        break;
                    default:
                        alert("Invalid key pressed!");
                    
                }
            }
            document.write("<div id = 'graph'>");
            document.write(xhr.responseText);
            document.write("</div>");
            document.write(BUTTONSTOANSWER)
            document.write("Player 1: Use A for left, S for right, D for midpoint, and F for trapezoidal.\n Player 2: Use ; for left, L for right, K for midpoint, and J for trapezoidal.");


            document.getElementById("answers").style = SHOWN;
            theIndexToStartSplicing += xhr.responseText.length;

            
        }else if (xhr.readyState === 4) {
            console.error("Failed to receive response:", xhr.status, xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
    alert("It may take up to a minute for data to load from the remote server!");
    
    
}

/*
function startGame(event) { //a new tester unworking
event.preventDefault();
var name1Element = document.getElementById("player1Name");
var name2Element = document.getElementById("player2Name");
var playerNameTable = document.getElementById("getTheData");
var graph = document.getElementById("graph");

var name1 = name1Element.value;
var name2 = name2Element.value;
var data = { "isGame": true, "name1": name1, "name2": name2 };

playerNameTable.style = HIDDEN;

var xhr = new XMLHttpRequest();
xhr.open("POST", "/submit", true);
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xhr.onreadystatechange = function () {
if (xhr.readyState === 4 && xhr.status === 200) {
    graph.innerHTML = xhr.responseText;
}
};
xhr.send(JSON.stringify(data));
}
*/
function processGameAnswer(player, option)
{
document.getElementById("answers").style = HIDDEN;
var xhr = new XMLHttpRequest();
xhr.open("POST", "/submit");
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
var data = {"identifier": MY_IDENTIFIER, "player": player, "option": option}
xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var element = document.body;
            //console.log(name1+name2+xhr.responseText)
            var bodyContent = element.innerHTML;
            //console.log(bodyContent)
            
            bodyContent = bodyContent.substring(0, bodyContent.indexOf("<div id"));
            console.log(bodyContent)
            //xhr.responseText
            document.body.id = "theBody";
            //document.write(bodyContent);
            document.body.onkeydown = function(ev)
            {
                key = ev.key;
                var oneLeft = document.getElementById("oneleft");
                var twoLeft = document.getElementById("twoleft");
                var oneRight = document.getElementById("oneright");
                var twoRight = document.getElementById("tworight");
                var oneMidpoint = document.getElementById("onemid");
                var twoMidpoint = document.getElementById("twomid");
                var oneTrapezoidal = document.getElementById("onetrap");
                var twoTrapezoidal = document.getElementById("twotrap")
                console.log("Key pressed: "+key)
                switch(key.toUpperCase())
                {
                    case PLAYER_1_LEFT:
                        oneLeft.click();
                        break;
                    case PLAYER_2_LEFT:
                        twoLeft.click();
                        break;
                    case PLAYER_1_RIGHT:
                        oneRight.click();
                        break;
                    case PLAYER_2_RIGHT:
                        twoRight.click();
                        break;
                    case PLAYER_1_MIDPOINT:
                        oneMidpoint.click();
                        break;
                    case PLAYER_2_MIDPOINT:
                        twoMidpoint.click();
                        break;
                    case PLAYER_1_TRAPEZOIDAL:
                        oneTrapezoidal.click();
                        break;
                    case PLAYER_2_TRAPEZOIDAL:
                        twoTrapezoidal.click();
                        break;
                    default:
                        alert("Invalid key pressed!");
                    
                }
            }
            document.getElementById("graph").remove()
            document.write("<div id = 'graph'>");
            document.write(xhr.responseText);
            document.write("Player 1: Use A for left, S for right, D for midpoint, and F for trapezoidal.\n Player 2: Use ; for left, L for right, K for midpoint, and J for trapezoidal.");

            //console.log(xhr.responseText)
            document.write("</div>");
            //document.write(BUTTONSTOANSWER);
            document.getElementById("answers").style = SHOWN;
            //theIndexToStartSplicing += xhr.responseText.length;
            

            
        }else if (xhr.readyState === 4) {
            console.error("Failed to receive response:", xhr.status, xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
    alert("It may take up to a minute for data to load from the remote server!");


}
