from splashScreen import SplashScreen
import tkinter as tk
import random
import playerAction
from networkSelector import UdpTransmitter
import psycopg2
import threading
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
        'dbname': 'photon',
        'password': 'student',
        'host': 'localhost'
    }
    
    try:
        conn = psycopg2.connect(**connection_params)
        return conn
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None

def insert_player_to_db(player_name, user_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO players (id, codename) VALUES (%s, %s);''', (int(user_id), player_name))
            conn.commit()
            print(f"Player {player_name} inserted into the database.")
        except Exception as error:
            print(f"Error inserting player into database: {error}")
        finally:
            cursor.close()
            conn.close()
#---------------------------------------------

#check or create user from database
def get_player_name_from_db(user_id):
    """Checks if a given user ID exists in the database and returns the player's name if found."""
    try:
        connection_params = {
            'dbname': 'photon',
            'password': 'student',
            'host': 'localhost'
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Use correct column names from the players table
        cursor.execute("SELECT codename FROM players WHERE id = %s;", (user_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  
        return None 
    
    except psycopg2.Error as e:
        print("Database error:", e)
        return None

    
    
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

    #----------------------------------------------
    # initialize player scores and B status
    players_scores = {
        "red1": {"score": 0, "has_B": False},
        "red2": {"score": 0, "has_B": False},
        "green1": {"score": 0, "has_B": False},
        "green2": {"score": 0, "has_B": False}
    }


    def update_score_and_B_status(player_name):
        # update score and check if player has B status
        if player_name in players_scores:
            player_data = players_scores[player_name]

            # update score when base hit
            player_data["score"] += 100

            # assign B status if not already given
            if not player_data["has_B"]:
                player_data["has_B"] = True
                return f"{player_name}: B"
            else:
                return player_name
        return player_name
    #----------------------------------------------


    def store_info():
        # both teams have 15 players.
        if team_counts["Red"] >= 15 and team_counts["Green"] >= 15:
            print("Teams are full. Cannot add more players.")
            return

        try:
            user_id = user_entry.get().strip()
            hardware_id = int(hardware_entry.get().strip())
            player_name = name_entry.get().strip()
        except ValueError:
            print("Hard ID must be an integer.")
            return
        
        if not user_id.isdigit():
            print("User ID must be a number.")
            return
        
        # Validate input
        if not str(user_id).isdigit() or not str(hardware_id).isdigit():
            print("Invalid input. Please enter a numeric user ID and hardware ID.")
            return


        # Check if the user ID exists in the database
        existing_player_name = get_player_name_from_db(user_id)


        if existing_player_name:
            print(f"User ID {user_id} already exists. Using existing player name: {existing_player_name}")
            player_name = existing_player_name  # Use the name from the database
        elif not player_name:
            print("New player requires a name.")
            return
        else:
            insert_player_to_db(player_name, user_id)  # Insert only if new


        # Assign team
        if hardware_id % 2 == 1 and team_counts["Red"] < 15:
            team = "Red"
        elif hardware_id % 2 == 0 and team_counts["Green"] < 15:
            team = "Green"
        else:
            print("No available teams. Cannot assign player.")
            return


        # Update player team
        player_teams[team].append((player_name, user_id, hardware_id))


        # Update UI
        row = team_counts[team] + 1
        grid = red_team_grid if team == "Red" else green_team_grid


        tk.Label(grid, text=player_name, bg="white", fg="black", width=15).grid(row=row, column=0)
        tk.Label(grid, text=user_id, bg="white", fg="black", width=15).grid(row=row, column=1)
        tk.Label(grid, text=hardware_id, bg="white", fg="black", width=15).grid(row=row, column=2)


        # Transmit player data via UDP
        message = f"{player_name}:{user_id}:{hardware_id}"
        try:
            udp_response = udp_transmitter.send_message(message)
            if udp_response:
                print("UDP response:", udp_response)
        except Exception as e:
            print("UDP transmission failed:", e)


        # Update team count
        team_counts[team] += 1


        print(f"Playername: {player_name}, User ID: {user_id}, Hardware ID: {hardware_id}, Team: {team}")


        # Check if teams are full
        if team_counts["Red"] == 15 and team_counts["Green"] == 15:
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
