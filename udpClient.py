from networkSelector import NetworkSelector, UdpTransmitter

def main():
    # Select the network 
    selector = NetworkSelector()
    selector.select_network()
    server_ip, server_port = selector.get_selected_network()

    # Create the transmitter.
    # client_port is set to 7501 
    transmitter = UdpTransmitter(ip=server_ip, port=server_port, client_port=7500)
    
    # Send the message to the server.
    if response:
        print("Message from Server:", response)

if __name__ == "__main__":
    main()
