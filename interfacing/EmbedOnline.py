
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

class MyServer(BaseHTTPRequestHandler):
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

            xArr, yArr, rienmannId, isGame, name1, name2 = self.parse_data(data)

            figure, html_content = self.generate_plot(xArr, yArr, rienmannId, isGame, name1, name2)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))

    def generate_plot(self, xArr, yArr, rienmannId, isGame, name1, name2):
        figure = plt.figure()
        appendages = ""

        if not isGame:
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
        else:
            player1 = Player(name1)
            player2 = Player(name2)
            myGame = Game(player1, player2)
            myGame.readyPlayers()
            myGame.generateFunction(randint(2, 6))
            myGame.setRandomCorrectAnswer()
            myGame.plot()
            
            myGame.makeNewBet()
            myGame.player1.betPoints(myGame.currentBet)
            myGame.player2.betPoints(myGame.currentBet)
            appendages += f"<h3>{myGame.player1.name}: {myGame.player1.points}</h3>\n<br/>"
            appendages += f"<h3>{myGame.player2.name}: {myGame.player2.points}</h3><br/>"
            appendages += f"<h3> Pot: {myGame.pot}</h3>"
        
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
        return xArr, yArr, rienmannId, isGame, name1, name2

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