import sys
import socket
from threading import Thread
from network_common.wrappers import Request, Response
from network_server.config import Configuration


class SKThread(Thread):
    """
    A class that provides the multithreading feature to the server
    along with the core logic of data transfer between server and client
    by the flow of byte stream.

    Arguments:
        obj(NetworkServer): the server object which needs to be multi-threaded.

    Methods:
        run:
            Enables multithreading for the provided object of obj
            and also governs the data transfer between the server and the client.
    """

    def __init__(self, obj):
        self.obj = obj
        Thread.__init__(self)
        self.start()

    def run(self):
        """
        This function executes the client requests in multithreaded fashion.
        Controls the transfer of bytes between client and server.
        First, the length of the request is received which in turn
        is used to receive the request data.
        This request data is passed to the requestHandler function
        and we obtain the response.
        This response is then further forwarded to the respective client
        in the same manager as the request was received by the server
        from the client.
        """
        databytes = b""
        to_recieve = 1024
        while len(databytes) < to_recieve:
            bytes_read = self.obj.client_socket.recv(
                to_recieve - len(databytes))
            databytes += bytes_read
        request_data_length = int(databytes.decode("utf-8").strip())
        databytes = b""
        to_recieve = request_data_length
        while len(databytes) < to_recieve:
            bytes_read = self.obj.client_socket.recv(
                to_recieve - len(databytes))
            databytes += bytes_read
        request_data = databytes.decode("utf-8")
        request = Request.from_json(request_data)
        response = self.obj.requestHandler(request)
        response_data = response.to_json()
        self.obj.client_socket.sendall(
            bytes(str(len(response_data)).ljust(1024), encoding="utf-8"))
        self.obj.client_socket.sendall(bytes(response_data, "utf-8"))
        self.obj.client_socket.close()


class NetworkServer:
    """
    A class which enables socket programming
    and controls the server-side of the network programming.

    Arguments:
        requestHandler(pointer to function): This is the pointer which gets invoked
        and processes the request data to generate the response data.

    Methods:
        initiate: This creates the server socket using the Python's socket module
        and binds it to the configuration object, which then connects to the client
        and is passed to the threading class SKThread.
    """

    def __init__(self, requestHandler):
        """
        The configuration gets loaded with the help of Configuration class
        and the pointer to function gets initialized. The configuration
        data is then validated latter the connection gets established.
        """
        self.server_conf = Configuration()
        self.requestHandler = requestHandler
        self.server_conf._obj._validate_values()
        if self.server_conf._obj.has_exceptions:
            for exception in self.server_conf._obj.exceptions:
                print(exception[1])
            sys.exit()

    def initiate(self):
        """
        This function creates a server socket using socket module of Python
        and connects it to the client with the help of a configuration object
        and thus is passed to SKThread class to make the server multithreaded.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", self.server_conf._obj.port))
        self.server_socket.listen()
        while True:
            print(
                f"Server is ready and listening at port {self.server_conf._obj.port}")
            self.client_socket, _ = self.server_socket.accept()
            SKThread(self)
        self.server_socket.close()
