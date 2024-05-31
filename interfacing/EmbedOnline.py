
from http.server import BaseHTTPRequestHandler, HTTPServer
import mpld3
import matplotlib.pyplot as plt
import json
import os
from random import randint
from backendgame import Tableality as Tableality
from backendgame.Tableality import Table
from backendgame.PlayersAndGame import Player, Game

hostName = "localhost"  # replace with the IP of the runner
serverPort = 8080
#myGame = Game(Player("default"), Player("default2"))
class BrowserSesh():
    def __init__(self,id):
        self.identifier = id
        self.myGame:Game = Game("default", "default2")

theListOfBrowserSessions:list[BrowserSesh] = []
class MyServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.myGame:Game = Game(Player("default"), Player("default2"))
        super(MyServer, self).__init__(request, client_address, server)
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(self.html_content(), "utf-8"))

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            print("Received data:", data)

            xArr, yArr, rienmannId, isGame, name1, name2, playerId, optionId, identifier = self.parse_data(data)
            print("Identifier", identifier)
            index = -1
            for i in theListOfBrowserSessions:
                if i.identifier == int(identifier):
                    index += 1
                    break
                index+=1
            if index < 0:
                index = len(theListOfBrowserSessions)
                theListOfBrowserSessions.append(BrowserSesh(identifier))
        
            
            figure, html_content = self.generate_plot(xArr, yArr, rienmannId, isGame, name1, name2, playerId, optionId, index)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))

    def generate_plot(self, xArr, yArr, rienmannId, isGame, name1, name2, playerId, optionId, index):
        figure = plt.figure()
        appendages = ""

        if not isGame and (playerId == -1 and optionId == -1):
            myTable = Table(xArr, yArr)
            startIndex = 0
            endIndex = len(xArr) - 1

            myTable.plot()
            if rienmannId == 0:
                Tableality.tableLeftRectangle(myTable, startIndex, endIndex)
            elif rienmannId == 1:
                Tableality.tableRightRectangle(myTable, startIndex, endIndex)
            elif rienmannId == 2:
                Tableality.tableMidpointRectangle(myTable, startIndex, endIndex)
            elif rienmannId == 3:
                Tableality.tableTrapezoids(myTable, startIndex, endIndex)
        elif isGame:
            print("isGame has executed.")
            player1 = Player(name1)
            player2 = Player(name2)
            theListOfBrowserSessions[index].myGame = Game(player1, player2)
            print(theListOfBrowserSessions[index].myGame.player1.name)
            theListOfBrowserSessions[index].myGame.readyPlayers()
            theListOfBrowserSessions[index].myGame.player1.myGame = theListOfBrowserSessions[index].myGame
            theListOfBrowserSessions[index].myGame.player2.myGame = theListOfBrowserSessions[index].myGame
            theListOfBrowserSessions[index].myGame.generateFunction(randint(2,3))
            theListOfBrowserSessions[index].myGame.setRandomCorrectAnswer()
            theListOfBrowserSessions[index].myGame.plot()
            print("Index", index)
            print("The list of browser sessions index myGame right answer", theListOfBrowserSessions[index].myGame.myCorrectAnswer)
            theListOfBrowserSessions[index].myGame.makeNewBet()
            theListOfBrowserSessions[index].myGame.player1.betPoints(theListOfBrowserSessions[index].myGame.currentBet)
            theListOfBrowserSessions[index].myGame.player2.betPoints(theListOfBrowserSessions[index].myGame.currentBet)
            appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player1.name}: {theListOfBrowserSessions[index].myGame.player1.points}</h3>\n<br/>"
            appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player2.name}: {theListOfBrowserSessions[index].myGame.player2.points}</h3><br/>"
            appendages += f"<h3> Pot: {theListOfBrowserSessions[index].myGame.pot}</h3>"
        elif playerId != -1 and optionId != -1:
            isRight = theListOfBrowserSessions[index].myGame.isRightAnswer(optionId)
            print("Is right line 95",isRight)
            print("Optionid line 96",optionId)
            print("My Correct line 97", theListOfBrowserSessions[index].myGame.myCorrectAnswer)
            print("listbrowserseshs",theListOfBrowserSessions)
            #print(theListOfBrowserSessions[index].myGame)
            if isRight:
                match(playerId):
                    case 1:
                        theListOfBrowserSessions[index].myGame.player1.receivePoints(theListOfBrowserSessions[index].myGame.pot)
                        theListOfBrowserSessions[index].myGame.pot = 0
                    case 2:
                        theListOfBrowserSessions[index].myGame.player2.receivePoints(theListOfBrowserSessions[index].myGame.pot)
                        theListOfBrowserSessions[index].myGame.pot = 0
            rand = randint(2,4)
            theListOfBrowserSessions[index].myGame.generateFunction(rand)
            #print(rand)

            theListOfBrowserSessions[index].myGame.setRandomCorrectAnswer()
            
            #print("myGame.player1", theListOfBrowserSessions[index].myGame.player1.name)
            #appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player1.name}: {theListOfBrowserSessions[index].myGame.player1.points}</h3>\n<br/>"
            #appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player2.name}: {theListOfBrowserSessions[index].myGame.player2.points}</h3><br/>"
            #appendages += f"<h3> Pot: {theListOfBrowserSessions[index].myGame.pot}</h3><br/>"
            if isRight:
                match(playerId):
                    case 1:
                        theListOfBrowserSessions[index].myGame.player1.receivePoints(theListOfBrowserSessions[index].myGame.pot)
                        theListOfBrowserSessions[index].myGame.pot = 0
                        appendages += f"<h3> Player 1 Wins The Points! Onto the next question...</h3>"
                    case 2:
                        theListOfBrowserSessions[index].myGame.player2.receivePoints(theListOfBrowserSessions[index].myGame.pot)
                        theListOfBrowserSessions[index].myGame.pot = 0
                        appendages += f"<h3> Player 2 Wins The Points! Onto the next question...</h3>"
            else:
                appendages += f"<h3> Nobody Wins The Points! They'll stay in the pot for the next question. Onto the next question...</h3>"
            playerWins = theListOfBrowserSessions[index].myGame.isWinnerReached()
            if(playerWins != False):
                match(playerWins):
                    case 1:
                        appendages += "<br/><h3>Player 1 wins! Thanks for playing!</h3>"
                    case 2:
                        appendages += "<br/><h3>Player 2 wins! Thanks for playing!</h3>"
            else:
                theListOfBrowserSessions[index].myGame.plot()
                theListOfBrowserSessions[index].myGame.makeNewBet()
                theListOfBrowserSessions[index].myGame.player1.myGame = theListOfBrowserSessions[index].myGame
                theListOfBrowserSessions[index].myGame.player2.myGame = theListOfBrowserSessions[index].myGame
                theListOfBrowserSessions[index].myGame.player1.betPoints(theListOfBrowserSessions[index].myGame.currentBet)
                theListOfBrowserSessions[index].myGame.player2.betPoints(theListOfBrowserSessions[index].myGame.currentBet)
                
                print("Pot", theListOfBrowserSessions[index].myGame.pot)
                #appendages = appendages.replace("<h3> Pot: 0</h3>",f"<h3>Pot: {theListOfBrowserSessions[index].myGame.pot}</h3>")
                
                appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player1.name}: {theListOfBrowserSessions[index].myGame.player1.points}</h3>\n<br/>"
                appendages += f"<h3>{theListOfBrowserSessions[index].myGame.player2.name}: {theListOfBrowserSessions[index].myGame.player2.points}</h3><br/>"
                appendages += f"<h3> Pot: {theListOfBrowserSessions[index].myGame.pot}</h3><br/>"
                #print("Index of the <h3> tag", appendages.index("<h3> Pot: 0</h3>"))
                print("Current bet 149", theListOfBrowserSessions[index].myGame.currentBet)
                print("Appendages:",appendages)

        
            


            

                    

        
        plt.ion()
        html_to_use = mpld3.fig_to_html(figure)
        html_content = f"""
        
            {appendages}
            {html_to_use}
            
       
        
        """
        #plt.close(figure)  # Close the figure to avoid memory issues
        return figure, html_content

    def parse_data(self, data):
        xArr = []
        yArr = []
        rienmannId = 0
        isGame = False
        name1 = ''
        name2 = ''
        playerId = -1
        optionId = -1
        identifier = ''
        for key, value in data.items():
            if key.startswith('x'):
                xArr.append(float(value))
            elif key.startswith('y'):
                yArr.append(float(value))
            elif key == 'rienmannId':
                rienmannId = int(value)
            elif key == 'isGame':
                isGame = True
            elif key == 'name1':
                name1 = value
            elif key == 'name2':
                name2 = value
            elif key == 'player':
                playerId = int(value)
            elif key == 'option':
                optionId = int(value)
            elif key == 'identifier':
                identifier = value
        return xArr, yArr, rienmannId, isGame, name1, name2, playerId, optionId, identifier

    def html_content(self):
        file_path = os.path.join(os.path.dirname(__file__), 'index.html')
        try:
            with open(file_path, "r") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")