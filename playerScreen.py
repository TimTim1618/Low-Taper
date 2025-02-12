from splashScreen import SplashScreen
import tkinter as tk
import random
import time
import playerAction

#insert informaiton into database
#--------------------------------------
#def add_player_to_db():
    #pass



#----------------------------------------
def playerScreen():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Player Screen")

    #team red

    left_frame = tk.Frame(root, bg='red', width=400, height=600)
    left_frame.pack(side='left', fill='both', expand=True)

    red_label = tk.Label(left_frame, text="Red Team", font = ("Arial", 24, "bold"), bg = "red", fg ="white")
    red_label.place(relx=0.5, rely=0.1,anchor="center")

    #team green

    right_frame = tk.Frame(root, bg='green', width=400, height=600)
    right_frame.pack(side='right', fill='both', expand=True)

    green_label = tk.Label(right_frame, text="Green Team", font = ("Arial", 24, "bold"), bg = "green", fg ="white")
    green_label.place(relx=0.5,rely=0.1, anchor="center")

    #Grid layout under teams
    red_team_grid = tk.Frame(left_frame, bg='red', width=400, height=400)
    red_team_grid.place(x=10, y=150)
    green_team_grid = tk.Frame(right_frame, bg='green', width=400, height=400)
    green_team_grid.place(x=10, y=150)

    #Display headers for grid
    tk.Label(red_team_grid, text="Player Name", bg="red", fg="white").grid(row=0, column=0)
    tk.Label(red_team_grid, text="Equipment ID", bg="red", fg="white").grid(row=0, column=1)
    tk.Label(green_team_grid, text="Player Name", bg="green", fg="white").grid(row=0, column=0)
    tk.Label(green_team_grid, text="Equipment ID", bg="green", fg="white").grid(row=0, column=1)


    #Enter information
    entry_label = tk.Label(left_frame, text="Enter your name:", bg="red", fg="white")
    entry_label.place(x=10, y=550)

    name_entry = tk.Entry(left_frame)
    name_entry.place(x=120, y=550)

    # Enter information for equipment ID
    equipment_label = tk.Label(left_frame, text="Enter equipment ID:", bg="red", fg="white")
    equipment_label.place(x=10, y=580)

    equipment_entry = tk.Entry(left_frame)
    equipment_entry.place(x=120, y=580)

    #Track player count
    team_counts = {"Red": 0, "Green":0}

    def store_info():
        # Randomly assign player to teams
        if team_counts["Red"] >= 2 and team_counts["Green"] >= 2:
            print("Both teams are full with two players!")
            return
        
        player_name = name_entry.get().strip()
        equipment_id = equipment_entry.get().strip()

        if not player_name or not equipment_id.isdigit():
            print("Invalid input. Please enter a name and a numeric equipment ID.")
            return

        # Determine team assignment
        available_teams = [team for team in ["Red", "Green"] if team_counts[team] < 2]
        team = random.choice(available_teams)

        row = team_counts[team] + 1  # Start from row 1 (row 0 is header)
        grid = red_team_grid if team == "Red" else green_team_grid
        color = "red" if team == "Red" else "green"

        tk.Label(grid, text=player_name, bg=color, fg="white").grid(row=row, column=0)
        tk.Label(grid, text=equipment_id, bg=color, fg="white").grid(row=row, column=1)

        team_counts[team] += 1

        # Check if teams are full
        if team_counts["Red"] == 2 and team_counts["Green"] == 2:
            print("Both teams are full. Ready to start!")

        # Clear the entry fields
        name_entry.delete(0, tk.END)
        equipment_entry.delete(0, tk.END)
#----------------------------------------------------------------
    #Submit button
    submit_button = tk.Button(left_frame, text="Submit", command=store_info)
    submit_button.place(x=300, y=565)

#----------------------------------------------------------------
    #Bind <F3> to transition to player screen
    def on_f3(event):
        playerAction.player_action_main(root)

#----------------------------------------------------------------
   
    root.bind("<F3>", on_f3)
    root.mainloop()

def main():
    SplashScreen()
    playerScreen()


if __name__ == "__main__":
    main()
