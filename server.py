import http.server

class RequestHandler(http.server.BaseHTTPRequestHandler):
    '''Returning a fixed page to handle HTTP requests'''
    
    Page = '''\
        <html>
        <body>
        <table>
            <tr> <td>Header</td>    <td>Value</td> </tr>
            <tr> <td>Date & Time</td>    <td>{date_time}</td> </tr>
            <tr> <td>Client host</td>    <td>{client_host}</td> </tr>
            <tr> <td>Client port</td>    <td>{client_port}</td> </tr>
            <tr> <td>Command</td>    <td>{command}</td> </tr>
            <tr> <td>Path</td>    <td>{path}</td> </tr>
        </table>
        </body>
        </html>
    '''
    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            'date_time' : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command' : self.command,
            'path' : self.path
        }
        page = self.Page.format(**values)
        return page


    #handling get requests
    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(bytes(page, 'utf-8'))

if __name__ == '__main__':
    serverAddress = ('', 7000)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
