import socket

class UdpTransmitter:
    def __init__(self, ip="127.0.0.1", port=20001):
        self.ip = ip
        self.port = port

    def set_network(self, ip, port):
        self.ip = ip
        self.port = port

    def send_message(self, message):
        bytes_to_send = str.encode(message)
        # Create a UDP socket
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        try:
            udp_socket.sendto(bytes_to_send, (self.ip, self.port))
            print(f"Sent message: '{message}' to {(self.ip, self.port)}")
        except Exception as e:
            print("Error sending UDP message:", e)
        finally:
            udp_socket.close()
