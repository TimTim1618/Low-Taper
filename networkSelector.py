import socket

class NetworkSelector:
    
    def __init__(self):
        self.predefined_networks = [
            ("Localhost", "127.0.0.1", 20001),
            ("Home Network", "192.168.1.100", 20001),
            ("Office Network", "10.0.0.50", 30000)
        ]
        self.selected_ip = "127.0.0.1"
        self.selected_port = 20001

    def select_network(self):
        print("\nSelect a network to connect to:")
        for i, (name, ip, port) in enumerate(self.predefined_networks, start=1):
            print(f"{i}. {name} ({ip}:{port})")
        print(f"{len(self.predefined_networks) + 1}. Enter custom network")

        try:
            choice = input(f"Enter your choice (1-{len(self.predefined_networks) + 1}): ")
        except EOFError:
            print("No input provided, using default network.")
            choice = "1"

        try:
            choice = int(choice)
            if 1 <= choice <= len(self.predefined_networks):
                self.selected_ip, self.selected_port = self.predefined_networks[choice - 1][1], self.predefined_networks[choice - 1][2]
            elif choice == len(self.predefined_networks) + 1:
                self.selected_ip = input("Enter IP address: ")
                self.selected_port = int(input("Enter Port number: "))
            else:
                print("Invalid choice. Using default network.")
        except ValueError:
            print("Invalid input. Using default network.")

        print(f"Selected Network: {self.selected_ip}:{self.selected_port}")

    def get_selected_network(self):
        return self.selected_ip, self.selected_port


class UdpTransmitter:
    
    def __init__(self, ip="127.0.0.1", port=20001, client_port=7501, buffer_size=1024):
        """
        ip: The destination server IP.
        port: The destination server port.
        client_port: The port from which the client sends messages.
        """
        self.ip = ip
        self.port = port
        self.client_port = client_port
        self.buffer_size = buffer_size

    def set_network(self, ip, port):
        """Set the network manually (e.g., from NetworkSelector)."""
        self.ip = ip
        self.port = port

    def send_message(self, message, receive_response=True):
        bytes_to_send = message.encode()
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        # Bind the socket to the designated client port.
        try:
            udp_socket.bind(("", self.client_port))
        except socket.error as e:
            print("Error binding to client port:", e)
            udp_socket.close()
            return None

        try:
            udp_socket.sendto(bytes_to_send, (self.ip, self.port))
            print(f"Sent message: '{message}' from client port {self.client_port} to {(self.ip, self.port)}")

            if receive_response:
                udp_socket.settimeout(2)  
                try:
                    response, server_address = udp_socket.recvfrom(self.buffer_size)
                    print(f"Received response from {server_address}: {response.decode()}")
                    return response.decode()
                except socket.timeout:
                    print("No response received from the server.")
        except socket.error as e:
            print("Error sending UDP message:", e)
        finally:
            udp_socket.close()
