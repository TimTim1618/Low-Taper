from splashScreen import SplashScreen
import tkinter as tk
import random
import playerAction
from networkSelector import UdpTransmitter
import psycopg2
from psycopg2 import sql

#---------------------------------------------
#information for data base
# player id = {player_name}
# user id = {user_id}
# hardware id = {hardware_id}
# team color = {team}

#--------------------------------------------

#---------------------------------------------
# Database connection setup
def connect_to_db():
    # Define connection parameters
    # We only need "photon" database
    connection_params = {
        'dbname': 'photon'
        # 'user': 'student',
        # 'password': 'student',
        # 'host': '127.0.0.1', #May need to be changed each time based on the VM ip address
        # 'port': '5432' # Uncomment if needed
    }
    
    try:
        conn = psycopg2.connect(**connection_params)
        return conn
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None

def insert_player_to_db(player_name, user_id, hardware_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO players (id, team, hardware) VALUES (%s, %s);''', (int(user_id), player_name,int(hardware_id)))
            conn.commit()
            print(f"Player {player_name} inserted into the database.")
        except Exception as error:
            print(f"Error inserting player into database: {error}")
        finally:
            cursor.close()
            conn.close()

#---------------------------------------------

def playerScreen():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Player Screen")

    # Main frames
    top_frame = tk.Frame(root)
    top_frame.pack(fill="both", expand=True)

    bottom_bar = tk.Frame(root, bg="white", height=80)
    bottom_bar.pack(fill="x")

    # Team Red
    left_frame = tk.Frame(top_frame, bg='red', width=400)
    left_frame.pack(side='left', fill='both', expand=True)

    red_label = tk.Label(left_frame, text="Red Team", font=("Arial", 24, "bold"), bg="red", fg="white")
    red_label.place(relx=0.5, rely=0.1, anchor="center")

    # Team Green
    right_frame = tk.Frame(top_frame, bg='green', width=400)
    right_frame.pack(side='right', fill='both', expand=True)

    green_label = tk.Label(right_frame, text="Green Team", font=("Arial", 24, "bold"), bg="green", fg="white")
    green_label.place(relx=0.5, rely=0.1, anchor="center")

    # Grid layout under teams
    red_team_grid = tk.Frame(left_frame, bg='red')
    red_team_grid.place(x=10, y=150)
    green_team_grid = tk.Frame(right_frame, bg='green')
    green_team_grid.place(x=10, y=150)

    # Display headers for grid
    tk.Label(red_team_grid, text="Player Name", bg="red", fg="white").grid(row=0, column=0)
    tk.Label(red_team_grid, text="User ID", bg="red", fg="white").grid(row=0, column=1)
    tk.Label(green_team_grid, text="Player Name", bg="green", fg="white").grid(row=0, column=0)
    tk.Label(green_team_grid, text="User ID", bg="green", fg="white").grid(row=0, column=1)
    tk.Label(red_team_grid, text="Hardware ID", bg="red", fg="white").grid(row=0, column=2)
    tk.Label(green_team_grid, text="Hardware ID", bg="green", fg="white").grid(row=0, column=2)

    # Input area inside white bottom bar
    entry_label = tk.Label(bottom_bar, text="Enter Playername:", bg="white", fg="black")
    entry_label.grid(row=0, column=0, padx=7, pady=5)

    name_entry = tk.Entry(bottom_bar)
    name_entry.grid(row=0, column=1, padx=7, pady=5)

    user_label = tk.Label(bottom_bar, text="Enter UserID:", bg="white", fg="black")
    user_label.grid(row=0, column=2, padx=7, pady=5)

    user_entry = tk.Entry(bottom_bar)
    user_entry.grid(row=0, column=3, padx=7, pady=5)

    hardware_label = tk.Label(bottom_bar, text="Enter HardwareID:", bg="white", fg="black")
    hardware_label.grid(row=0, column=4, padx=7, pady=5)

    hardware_entry = tk.Entry(bottom_bar, text = "Enter HardwareID", bg = "white", fg = "black")
    hardware_entry.grid(row=0, column=5, padx=7, pady=5)

    #track player count
    team_counts = {"Red": 0, "Green": 0}

    #create a Udp transmitter instence
    udp_transmitter = UdpTransmitter()


    player_teams = {"Red": [], "Green": []}

    def store_info():
        """Randomly assigns a player to a team until both teams have 2 players."""
        if team_counts["Red"] >= 2 and team_counts["Green"] >= 2:
            print("Teams are full. Cannot add more players.")
            return

        player_name = name_entry.get().strip()
        user_id = user_entry.get().strip()
        hardware_id = hardware_entry.get().strip() 

        if not player_name or not user_id.isdigit() or not hardware_id.isdigit():
            print("Invalid input. Please enter a name, numeric user ID, and numeric hardware ID.")
            return

        insert_player_to_db(player_name, user_id, hardware_id)

        # Determine team assignment
        available_teams = [team for team in ["Red", "Green"] if team_counts[team] < 2]
        team = random.choice(available_teams)

        # Add player to the correct team in dictionary
        player_teams[team].append((player_name, user_id))

        row = team_counts[team] + 1
        grid = red_team_grid if team == "Red" else green_team_grid
        color = "red" if team == "Red" else "green"

        tk.Label(grid, text=player_name, bg="white", fg="black", width=15).grid(row=row, column=0)
        tk.Label(grid, text=user_id, bg="white", fg="black", width=15).grid(row=row, column=1)
        tk.Label(grid, text=hardware_id, bg="white", fg="black", width=15).grid(row=row, column=2)

        # Transmit player name, user ID, and hardware ID to UDP server
        message = f"{player_name}:{user_id}:{hardware_id}"
        udp_response = udp_transmitter.send_message(message)
        if udp_response:
            print("UDP response:", udp_response)

        team_counts[team] += 1

        print(f"Playername: {player_name}, User ID: {user_id}, Hardware ID: {hardware_id}, Team: {team}")

        # Check if teams are full
        if team_counts["Red"] == 2 and team_counts["Green"] == 2:
            print("Both teams are full. Ready to start!")

        # Clear input fields
        name_entry.delete(0, tk.END)
        user_entry.delete(0, tk.END)
        hardware_entry.delete(0, tk.END)

    # Submit button
    submit_button = tk.Button(bottom_bar, text="Submit", command=store_info)
    submit_button.grid(row=0, column=6, padx=10, pady=5)

    #tell user to press f3
    f3_label = tk.Label(left_frame, text="F3 Start Game", font=("Arial", 10, "bold"), fg="black", bg="red")
    f3_label.place(x=10, y=500)
    #tell the user to press f12 to clear the screen
    f12_label = tk.Label(left_frame, text="F12 Clear Players", font = ("Arial", 10, "bold"), fg = "black", bg = "red")
    f12_label.place(x=10, y=525)

    # Remove players from player screen 
    def on_f12(event):
        for team in ["Red", "Green"]:
            player_teams[team].clear()
            team_counts[team] = 0


        for widget in red_team_grid.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        for widget in green_team_grid.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        #clear input fields
        name_entry.delete(0, tk.END)
        user_entry.delete(0, tk.END)
        hardware_entry.delete(0, tk.END)

        print("All players removed!")

    root.bind("<F12>", on_f12)

    # Bind <F3> to transition to player action screen
    def on_f3(event):
        player_action_screen()
    def player_action_screen():
        print("Transitioning to Player Action Screen!")
        playerAction.player_action_main(root, player_teams)
        
    root.bind("<F3>", on_f3)
    root.mainloop()

def main():
    SplashScreen()
    playerScreen()


if __name__ == "__main__":
    main()
