import playerScreen
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pygame
import os
import time

def player_action_main(previous_window, player_teams):
    previous_window.destroy()
    countdown_timer(player_teams)

def countdown_timer(player_teams):
    countdown_window = tk.Tk()
    countdown_window.title("Countdown")
    countdown_window.geometry("800x600")
    countdown_window.configure(bg="black")

    # Label to display countdown images
    countdown_label = Label(countdown_window, bg="black")
    countdown_label.pack(expand=True)

    #play audio for countdown
    pygame.mixer.init()
    # sound_path = os.path.join("photon_tracks", "Track01.mp3")
    # pygame.mixer.Sound(sound_path).play()

    image_folder = "countdown_images"

    # Load background image
    background_path = os.path.join(image_folder, "background.tif")
    background = Image.open(background_path) if os.path.exists(background_path) else None

    # Load alert image
    alert_path = os.path.join(image_folder, "alert-on.tif")
    alert_img = Image.open(alert_path) if os.path.exists(alert_path) else None
    alert_img = alert_img.resize((800, 600)) if alert_img else None
    alert_img = ImageTk.PhotoImage(alert_img) if alert_img else None

    # Load countdown images with numbers overlaid on the background
    countdown_images = []
    for i in range(30, -1, -1): 
        num_path = os.path.join(image_folder, f"{i}.tif")
        if background and os.path.exists(num_path):
            num_img = Image.open(num_path).convert("RGBA")
            
            # Overlay the countdown number onto the background
            combined = background.copy().convert("RGBA")
            num_img = num_img.resize((100, 100))  
            num_position = ((combined.width - num_img.width) // 2, ((combined.height - num_img.height) // 2) + 50)

            combined.paste(num_img, num_position, num_img)

            countdown_images.append(ImageTk.PhotoImage(combined))
        


    def update_countdown(index):
        if index == -1 and alert_img:
            countdown_label.config(image=alert_img)
            countdown_window.after(1000, update_countdown, 0)
        elif index < len(countdown_images):
            countdown_label.config(image=countdown_images[index])
            countdown_window.after(1000, update_countdown, index + 1)
        # elif index == 20:
        #     track_path = os.path.join("photon_tracks", "Track02.mp3")
        #     pygame.mixer.music.load(track_path)
        #     pygame.mixer.music.play()
        else:
            countdown_window.destroy() 
            action_log(player_teams) 
        
    update_countdown(-1) 
    countdown_window.mainloop()

def action_log(player_teams):
    action_window = tk.Tk()
    action_window.title("Player Action")
    action_window.geometry("800x600")
    action_window.configure(bg="black")

    # Top frame for team scores
    top_frame = tk.Frame(action_window, bg='black')
    top_frame.pack(fill="x", padx=10, pady=5)

    left_team_frame = tk.Frame(top_frame, bg='black')
    left_team_frame.pack(side='left', expand=True)

    right_team_frame = tk.Frame(top_frame, bg='black')
    right_team_frame.pack(side='right', expand=True)

    tk.Label(left_team_frame, text="RED TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()
    tk.Label(right_team_frame, text="GREEN TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()

    # Initialize scores for each player and display them
    player_scores = {}

    for index, (name, _) in enumerate(player_teams["Red"], start=1):
        player_scores[f"red_player{index}_score"] = 0  # Start with score 0
        tk.Label(left_team_frame, text=f"{name} - Score: {player_scores[f'red_player{index}_score']}", 
                 font=("Arial", 14), fg="red", bg="black").pack()
    
    for index, (name, _) in enumerate(player_teams["Green"], start=1):
        player_scores[f"green_player{index}_score"] = 0  # Start with score 0
        tk.Label(right_team_frame, text=f"{name} - Score: {player_scores[f'green_player{index}_score']}", 
                 font=("Arial", 14), fg="green", bg="black").pack()

    # Middle frame for game actions
    middle_frame = tk.Frame(action_window, bg='black', highlightbackground="yellow", highlightthickness=2)
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(middle_frame, text="Current Game Action", font=("Arial", 14, "bold"), fg="white", bg="black").pack()

    # Action Log
    action_log_frame = tk.Frame(middle_frame, bg="black")
    action_log_frame.pack(fill="both", expand=True)

    action_log = tk.Text(action_log_frame, height=10, bg="blue", fg="white", font=("Arial", 12, "italic"), wrap="word")
    action_log.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(action_log_frame, command=action_log.yview)
    scrollbar.pack(side="right", fill="y")
    action_log.config(yscrollcommand=scrollbar.set)

    # Bottom frame for timer
    bottom_frame = tk.Frame(action_window, bg='black')
    bottom_frame.pack(fill="x", padx=10, pady=5)

    timer_label = tk.Label(bottom_frame, text="Time Remaining: 3:00", font=("Arial", 16, "bold"), fg="white", bg="black")
    timer_label.pack()

    # Switch back to player screen
    def on_f1(event):
        action_window.destroy()
        playerScreen.playerScreen()
    
    action_window.bind("<F1>", on_f1)

    # f1_button = tk.Button(action_window, text="Start", command=on_f1)
    # f1_button.pack(pady=20)

    action_window.mainloop()
