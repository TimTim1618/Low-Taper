import socket
from networkSelector import NetworkSelector

def main():
    #choosing the network here 
    selector = NetworkSelector()
    selector.select_network()
    localIP, localPort = selector.get_selected_network()

    # Create a UDP socket and bind it to the selected server IP and port.
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    try:
        UDPServerSocket.bind((localIP, localPort))
    except socket.error as e:
        print(f"Error binding server socket to {localIP}:{localPort}: {e}")
        return

    print(f"UDP server up and listening on {localIP}:{localPort}")

    bufferSize = 1024

    while True:
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client: {}".format(message.decode())
            clientIP  = "Client IP Address: {}".format(address)
            
            print(clientMsg)
            print(clientIP)

            #reply to the client.
            UDPServerSocket.sendto(bytesToSend, address)
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break

    UDPServerSocket.close()

if __name__ == "__main__":
    main()
