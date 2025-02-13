from networkSelector import NetworkSelector, UdpTransmitter

def main():
    # Select the network (this sets the destination server IP/port).
    selector = NetworkSelector()
    selector.select_network()
    server_ip, server_port = selector.get_selected_network()

    # Create the transmitter.
    # client_port is set to 7501 (so the UDP packet is transmitted from port 7501).
    transmitter = UdpTransmitter(ip=server_ip, port=server_port, client_port=7501)
    
    # Send the message to the server.
    response = transmitter.send_message("Hello UDP Server")
    if response:
        print("Message from Server:", response)

if __name__ == "__main__":
    main()
