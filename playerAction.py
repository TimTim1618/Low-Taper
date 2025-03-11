import playerScreen
import tkinter as tk
from tkinter import Label, Frame, Text, Scrollbar, Button

def player_action_main(previous_window, player_teams):
    previous_window.destroy()  # Close the previous window

    action_window = tk.Tk()
    action_window.title("Player Action")
    action_window.geometry("800x600")
    action_window.configure(bg="black")

    # Top frame for team scores
    top_frame = Frame(action_window, bg='black')
    top_frame.pack(fill="x", padx=10, pady=5)

    left_team_frame = Frame(top_frame, bg='black')
    left_team_frame.pack(side='left', expand=True)

    right_team_frame = Frame(top_frame, bg='black')
    right_team_frame.pack(side='right', expand=True)

    Label(left_team_frame, text="RED TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()
    Label(right_team_frame, text="GREEN TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()

    # Display Players in Teams
    for name, equipment_id in player_teams["Red"]:
        Label(left_team_frame, text=f"{name} - {equipment_id}", font=("Arial", 14), fg="red", bg="black").pack()
    
    for name, equipment_id in player_teams["Green"]:
        Label(right_team_frame, text=f"{name} - {equipment_id}", font=("Arial", 14), fg="green", bg="black").pack()

    # Middle frame for game actions
    middle_frame = Frame(action_window, bg='black', highlightbackground="yellow", highlightthickness=2)
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    Label(middle_frame, text="Current Game Action", font=("Arial", 14, "bold"), fg="white", bg="black").pack()

    # Action Log
    action_log_frame = Frame(middle_frame, bg="black")
    action_log_frame.pack(fill="both", expand=True)

    action_log = Text(action_log_frame, height=10, bg="blue", fg="white", font=("Arial", 12, "italic"), wrap="word")
    action_log.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(action_log_frame, command=action_log.yview)
    scrollbar.pack(side="right", fill="y")
    action_log.config(yscrollcommand=scrollbar.set)

    # Bottom frame for timer
    bottom_frame = Frame(action_window, bg='black')
    bottom_frame.pack(fill="x", padx=10, pady=5)

    timer_label = Label(bottom_frame, text="Time Remaining: 3:00", font=("Arial", 16, "bold"), fg="white", bg="black")
    timer_label.pack()

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
    # action_window.mainloop()

    

#-----------------------------------


    #pass
