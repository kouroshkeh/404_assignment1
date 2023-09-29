#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2023 Kourosh Kehtari
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print("Got a request of: %s\n" % self.data)
        if self.data.split("\r\n")[0].split()[0] == "GET":
            response = self.get_request(self.data.split("\r\n")[0].split()[1])
        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        self.request.sendall(response.encode('utf-8'))
    def get_request(self, path):
        if not path.endswith('/') and '.' not in path.split('/')[-1]:
            return f"HTTP/1.1 301 Moved Permanently\r\nLocation: {path}/\r\n\r\n"
        if path.endswith('/'): path += "index.html"
        if os.path.isfile(os.path.join("www", path[1:])):
            if os.path.splitext(os.path.join("www", path[1:]))[1] == ".html":
                mime = "text/html"
            else:
                mime = "text/css"
            with open(os.path.join("www", path[1:]), 'r') as f:
                read = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\n\r\n{read}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found!"
        return response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    server.serve_forever()
