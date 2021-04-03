import sys
from network_client.config import Configuration
from network_common.wrappers import Request, Response
import socket


class NetworkClient:
    """
    A class which enables socket programming
    and controls the client-side of the network programming.

    Method:
        send(request): This method takes the request object and sends
        it to the server and then receives the response from the server.
    """

    def __init__(self):
        self.server_configuration = Configuration()
        self.server_configuration._obj._validate_values()
        if self.server_configuration._obj.has_exceptions:
            for exception in self.server_configuration._obj.exceptions.values():
                print(exception[1])
            sys.exit()  # needs to be converted to code raises exceptions.

    def send(self, request):
        """
        It connects the client socket to the server socket and sends
        request to it while receiving the response.
        It receives a response(JSON String) and then converts it into a Response class
        object.

        Return Value:
            returns a Response class object.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_configuration._obj.host, self.server_configuration._obj.port))
        request_data = request.to_json()
        client_socket.sendall(bytes(str(len(request_data)).ljust(1024), encoding="utf-8"))
        client_socket.sendall(bytes(request_data, encoding="utf-8"))
        databytes = b""
        to_recieve = 1024
        while len(databytes) < to_recieve:
            dbytes = client_socket.recv(to_recieve - len(databytes))
            databytes += dbytes
        response_data_length = int(databytes.decode("utf-8").strip())
        databytes = b""
        to_recieve = response_data_length
        while len(databytes) < to_recieve:
            dbytes = client_socket.recv(to_recieve - len(databytes))
            databytes += dbytes
        response_data = databytes.decode("utf-8")
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        response = Response.from_json(response_data)
        return response
