import sys
import socket

class NetworkSelector:
    def __init__(self):
        self.predefined_networks = ["127.0.0.1"]
        self.selected_ip = "127.0.0.1"

    def select_network(self):
        print("\nSelect a network to connect to:")
        for i, ip in enumerate(self.predefined_networks, start=1):
            print(f"{i}. {ip}")
        print(f"{len(self.predefined_networks) + 1}. Enter custom network")

        try:
            choice = input(f"Enter your choice (1-{len(self.predefined_networks) + 1}): ")
            choice = int(choice)
            if 1 <= choice <= len(self.predefined_networks):
                self.selected_ip = self.predefined_networks[choice - 1]
            elif choice == len(self.predefined_networks) + 1:
                self.selected_ip = input("Enter IP address: ")
            else:
                print("Invalid choice. Using default network.")
        except ValueError:
            print("Invalid input. Using default network.")

        print(f"Selected Network: {self.selected_ip}")

    def get_selected_network(self):
        return self.selected_ip

class UdpTransmitter:
    def __init__(self, ip="127.0.0.1", send_port=7500, listen_port=7501, buffer_size=1024):
        self.ip = ip
        self.send_port = send_port
        self.listen_port = listen_port
        self.buffer_size = buffer_size
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(("", self.listen_port))

    def set_network(self, ip):
        self.ip = ip

    def send_message(self, message):
        bytes_to_send = message.encode()
        try:
            self.udp_socket.sendto(bytes_to_send, (self.ip, self.send_port))
            print(f"Sent message: '{message}' to {(self.ip, self.send_port)}")
        except socket.error as e:
            print("Error sending UDP message:", e)

    def listen_for_response(self):
        try:
            print("Listening for responses...")
            response, server_address = self.udp_socket.recvfrom(self.buffer_size)
            print(f"Received response from {server_address}: {response.decode()}")
            return response.decode()
        except socket.timeout:
            print("No response received.")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    else:
        selector = NetworkSelector()
        selector.select_network()
        ip = selector.get_selected_network()

    transmitter = UdpTransmitter(ip=ip)
    transmitter.send_message("Hello, network!")
