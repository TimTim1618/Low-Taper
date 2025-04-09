import socket
import logging
from networkSelector import NetworkSelector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    selector = NetworkSelector()
    selector.select_network()
    localIP, localPort = selector.get_selected_network()

    # Default to 127.0.0.1 unless changed by user
    if not selector.network_changed_by_user():
        localIP = "127.0.0.1"

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        UDPServerSocket.bind((localIP, localPort))
    except socket.error as e:
        logging.error(f"Error binding server socket to {localIP}:{localPort}: {e}")
        return

    logging.info(f"UDP server up and listening on {localIP}:{localPort}")

    bufferSize = 1024
    UDPServerSocket.settimeout(2)  # Prevents blocking indefinitely

    try:
        while True:
            try:
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                message = bytesAddressPair[0].decode()
                address = bytesAddressPair[1]

                logging.info(f"Message from Client: {message}")
                logging.info(f"Client IP Address: {address}")

                # Define the response before sending it
                response_message = f"Received: {message}"
                UDPServerSocket.sendto(response_message.encode(), address)

            except socket.timeout:
                pass  # Prevents freezing when there's no incoming message

            except socket.error as e:
                logging.warning(f"Error receiving data: {e}")

    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        UDPServerSocket.close()

if __name__ == "__main__":
    main()
