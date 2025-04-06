import http.server
import os

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

    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(str(content))
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def do_GET(self):
        try:
            fullPath = os.getcwd() + self.path

            if not os.path.exists(fullPath):
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(fullPath):
                self.handle_file(fullPath)
            else:
                raise ServerException("Unknown object '{0}".format(self.path))

        except Exception as msg:
            self.handle_error(msg)

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
