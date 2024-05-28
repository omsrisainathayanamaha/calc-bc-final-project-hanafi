#https://stackoverflow.com/questions/49684811/display-matplotlib-graph-in-browser

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import mpld3
import matplotlib
from matplotlib import pyplot as plt
import json
import backendgame.Tableality as Tableality
from backendgame.Tableality import Table

hostName = "10.7.131.245" #replace with the ip of the runner
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
            
            xArr, yArr, id = self.parse_data(data)
            #print("xArr:", xArr)
            #print("yArr:", yArr)
            myTable = Table(xArr, yArr)
            startIndex = 0
            endIndex = len(xArr)-1
            figure = plt.figure()
            self.send_response(200)
            #self.send_header("Content-type", "application/json")
            #self.end_headers()
            #response = {"status": "success", "xArr": xArr, "yArr": yArr}
            #self.wfile.write(bytes(json.dumps(response), "utf-8"))
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
            #Tableality.tableLeftRectangle(myTable, startIndex, endIndex)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write (bytes(mpld3.fig_to_html(figure, d3_url=None, mpld3_url=None, no_extras=False, template_type='general', figid=None, use_http=False), "utf-8"))

            
            

    def parse_data(self, data):
        xArr = []
        yArr = []
        rienmannId = 0
        for key, value in data.items():
            if key.startswith('x'):
                xArr.append(float(value))
            elif key.startswith('y'):
                yArr.append(float(value))
            elif key.startswith('rienmann'):
                rienmannId = int(value)
        return xArr, yArr, rienmannId

    def html_content(self):
        return """<!DOCTYPE html>
<html>
<head>
    <script>
        function doSubmit() {
            var selectMe = document.getElementById('selectme');
            var value = selectMe.value;
            if (value == 0) {
                createTable(parseInt(prompt('How many elements?')));
            }
        }

        function createTableRow(id1, id2) {
            var elementTr = document.createElement('tr');
            var template1 = document.createElement('td');
            var input1 = document.createElement('input');
            input1.type = 'text';
            input1.id = id1;
            input1.value = Math.round(Math.random() * 100);
            template1.appendChild(input1);
            elementTr.appendChild(template1);
            var template2 = document.createElement('td');
            var input2 = document.createElement('input');
            input2.type = 'text';
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
            var data = {};

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
                    //var element = document.getElementById('results')
                    document.write(xhr.responseText);
                    
                }
            };
            xhr.send(JSON.stringify(data));
        }
    </script>
</head>
<body>
    <h1>Select an option</h1>
    <br/>
    <select id='selectme'>
        <option value=0>Calculator</option>
        <option value=1>Game</option>
    </select><br/>
    <button onclick='doSubmit()'>Submit!</button>
    <br/><br/>
    <table id='theInputTable'>
        <tr>
            <th>x</th>
            <th>y</th>
        </tr>
    </table>
    <br/>
    <select id = "theSelection">
        <option value = 0>Left Rienmann Sum</option>
        <option value = 1>Right Rienmann Sum</option>
        <option value = 2>Midpoint Rienmann Sum</option>
        <option value = 3>Trapezoidal Rienmann Sum</option>
    </select>
    <button onclick='sendData()'>Send Data</button>
    <div id = 'results'></div>
</body>
</html>"""

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
