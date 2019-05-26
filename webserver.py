from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
from searchengine import SearchEngine
"""
This is a response, that server sends back to the client
1st peace without from and data
"""
resp = """<html>
    <head>
        <title>ASXER (Anya's Super indeXER)</title>
        <style>
            body{background-color: #2F4F4F;font-family: sans-serif; color: #B8860B;}
            h1{border-bottom: 3px solid #DAA520;padding-bottom: 5px;}
            input{font-size: 14px; border: 3px solid #C71585;border-radius: 20px;padding: 6px; background-color: #2F4F4F;color:#FFB6C1;;width: 70%}
            input:focus{outline: none;}
            input[type=submit]{background-color: #C71585;width: auto;}
            strong{color:#DC143C;}
            ol{text-align: left;}
        </style>
    </head>"""
data="""<body>
        <div align="center">
            <form method="post">
                <h1>Enter query to search</h1>
                <input type="text" name="query" value="{0}">
                <input type="submit" value="SEARCH">
            </form>
            {1}<br><br>
            <sub>&copy; ASXER (Anya's Super indeXER)</sub>
        </div>
    </body>
</html>
"""

class WebServer(BaseHTTPRequestHandler):
    """
    This class is used for request handling in our searchengine
    """
    def do_GET(self):
        """
        Defaut get request from client to get site
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes((resp + data.format ('','')), "utf-8"))
    def do_POST(self):
        """
        POST handler for query
        """
        try:
            content_length = int(self.headers['Content-Length'])
            body = str(self.rfile.read(content_length))
            query = unquote(body.split('=')[1][:-1])

            search_engine = SearchEngine('warandpeace')
            r = search_engine.search_to_highlight(query, 4)

            myresp = '<ol>\n'
            for key in r.keys():
                myresp += '<li>'+key+'</li>\n<ul>'
                for val in r[key]:
                    myresp += '<li>'+val+'</li>'
                myresp += '</ul>'
            myresp += '</ol>'

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes((resp + data.format (query,myresp)), "utf-8"))
        except:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes((resp + data.format ('','Not Found')), "utf-8"))

# Start HTTP server on global IP and 80 port
ws = HTTPServer(('0.0.0.0', 80), WebServer)

# Server running until Ctrl-C pressed
try:
    ws.serve_forever()
except KeyboardInterrupt:
    pass

ws.server_close()