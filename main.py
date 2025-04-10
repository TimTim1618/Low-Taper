import subprocess
import sys

def check_python_installed():
    try:
        # Try to check if Python is available
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Python is already installed.")
        return True
    except subprocess.CalledProcessError:
        # If Python isn't found, it will try to install it
        print("Python is not installed. Installing Python...")
        return False

def install_python():
    # Install Python via Winget
    subprocess.run(["winget", "install", "Python.Python.3"], check=True)

def main():
    # Check if Python is installed
    if not check_python_installed():
        # Install Python if not found
        install_python()

    print("Select a network to connect to:")
    print("1. Localhost (127.0.0.1:7501)")
    print("2. Enter custom network")
    
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        ip = "127.0.0.1"
        port = "7501"
    elif choice == "2":
        ip = input("Enter IP address: ").strip()
        port = input("Enter Port number: ").strip()
    else:
        print("Invalid choice, defaulting to localhost.")
        ip = "127.0.0.1"
        port = "7501"

    print(f"Selected Network: {ip}:{port}")
    
    # Run the playerScreen.py with the given IP and port
    subprocess.run(["python", "playerScreen.py", ip, port])

if __name__ == "__main__":
    main()
