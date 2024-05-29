#https://stackoverflow.com/questions/49684811/display-matplotlib-graph-in-browser

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import mpld3
import matplotlib
from matplotlib import pyplot as plt
import json
import backendgame.Tableality as Tableality
from backendgame.Tableality import Table
import os
from backendgame.PlayersAndGame import Player as Player
from backendgame.PlayersAndGame import Game as Game
from backendgame import PlayersAndGame
from random import randint
hostName = "localhost" #replace with the ip of the runner
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
            print("Received data:", data)  # Here you can process the data as needed
            
            xArr, yArr, id, isGame, name1, name2 = self.parse_data(data)
            myGame = None
            figure = plt.figure()
            #print("xArr:", xArr)
            #print("yArr:", yArr)
            if(not isGame):
                myTable = Table(xArr, yArr)
                startIndex = 0
                endIndex = len(xArr)-1
                
                self.send_response(200)
            
                myTable.plot()
                match id:
                    case 0:
                        Tableality.tableLeftRectangle(myTable, startIndex, endIndex)
                    case 1:
                        Tableality.tableRightRectangle(myTable, startIndex, endIndex)
                    case 2:
                        Tableality.tableMidpointRectangle(myTable, startIndex, endIndex)
                    case 3:
                        Tableality.tableTrapezoids(myTable, startIndex, endIndex)
            
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                player1 = Player(name1)
                player2 = Player(name2)
                myGame = Game(player1, player2)
                myGame.readyPlayers()
                myGame.generateFunction(randint(2,6))
                
                
            htmlToUse = mpld3.fig_to_html(figure, d3_url=None, mpld3_url=None, no_extras=False, template_type='general', figid=None, use_http=False) 
            htmlToUse = htmlToUse.replace("<html>", "")
            htmlToUse = htmlToUse.replace("</html>", "")
            htmlToUse=htmlToUse.replace("<head>", "")
            htmlToUse=htmlToUse.replace("</head>", "")
            htmlToUse=htmlToUse.replace("<body>", "")
            htmlToUse=htmlToUse.replace("</body>", "")
            plt.ion()
            self.wfile.write (bytes(htmlToUse,"utf-8"))

            
            

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
            elif key.startswith('rienmann'):
                rienmannId = int(value)
            elif key.startswith('isGa'):
                isGame = True
            elif key == 'name1':
                name1 = value
            elif key == 'name2':
                name2 = value
        return xArr, yArr, rienmannId, isGame, name1, name2

    def html_content(self):
        # Ensure the correct path to the file
        file_path = os.path.join(os.path.dirname(__file__), 'index.html')

        # Read the file contents safely
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
