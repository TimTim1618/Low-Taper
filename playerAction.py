import playerScreen
import tkinter as tk
from tkinter import Frame, Label, Text

#action menu
#-----------------------------------    
def player_action_main(previous_window, player_teams):
    previous_window.destroy()  # Close the previous window

    action_window = tk.Tk()
    action_window.title("Player Action")
    action_window.geometry("800x600")
    action_window.configure(bg="black")

    top_frame = tk.Frame(action_window, bg='black')
    top_frame.pack(fill="x", padx=10, pady=5)

    left_team_frame = tk.Frame(top_frame, bg='black')
    left_team_frame.pack(side='left', expand=True)

    right_team_frame = tk.Frame(top_frame, bg='black')
    right_team_frame.pack(side='right', expand=True)

    tk.Label(left_team_frame, text="RED TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()
    tk.Label(right_team_frame, text="GREEN TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()

    # Display Players in Teams
    for name, equipment_id in player_teams["Red"]:
        tk.Label(left_team_frame, text=f"{name} - {equipment_id}", font=("Arial", 14), fg="red", bg="black").pack()
    
    for name, equipment_id in player_teams["Green"]:
        tk.Label(right_team_frame, text=f"{name} - {equipment_id}", font=("Arial", 14), fg="green", bg="black").pack()

    action_window.mainloop()
    
    #switch back to player Screen
    def on_f1(event):
        action_window.destroy()
        playerScreen.playerScreen()
    f1_button = tk.Button(action_window, text="Player Screen", command = on_f1)
    f1_button.pack(pady=20)

    # #start button
    # def on_f4(event):
    #     #function goes here

    # #f4 start button stuff. Starts countdown and music
    # f4_button = tk.Button(action_window, text="Start Countdown (f4)", command = #countdown and musci function goes here )
    # f4_button.pack(pady=20)   

    # action_window.bind("<F1>", on_f1)

    # action_window.bind("<F4>", on_f4)
    action_window.mainloop()

    

#-----------------------------------


    #pass