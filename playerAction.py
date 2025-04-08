import playerScreen
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pygame
import os
import time
import random
import threading

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
    #countdown set at 3 seconds until we turn it in... then change it to 30.
    for i in range(1, -1, -1): 
        num_path = os.path.join(image_folder, f"{i}.tif")
        if background and os.path.exists(num_path):
            num_img = Image.open(num_path).convert("RGBA")
            
            # Overlay the countdown number onto the background
            combined = background.copy().convert("RGBA")
            num_img = num_img.resize((100, 100))  
            num_position = ((combined.width - num_img.width) // 2, ((combined.height - num_img.height) // 2) + 50)

            combined.paste(num_img, num_position, num_img)

            countdown_images.append(ImageTk.PhotoImage(combined))


    # def play_track(track_path):
    #     pygame.mixer.music.load(track_path)  # Load the audio file
    #     pygame.mixer.music.play()  # Play the audio
    #     print(f"Now playing: {os.path.basename(track_path)}")  # Display the track name



    def update_countdown(index):
        if index == -1 and alert_img:
            countdown_label.config(image=alert_img)
            countdown_window.after(1000, update_countdown, 0)
    #Audio for countdown / we will implement this when needed in future sprints 
        elif index == 12:
            pygame.mixer.init()
             #play audio for countdown
            MUSIC_FOLDER = "photon_tracks"
            sound_files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]
            random.shuffle(sound_files)
            if sound_files:
                # play_track(sound_files[0])
                print("hello")
            countdown_label.config(image=countdown_images[index])
            countdown_window.after(1000, update_countdown, index + 1)
        elif index < len(countdown_images):
            countdown_label.config(image=countdown_images[index])
            countdown_window.after(1000, update_countdown, index + 1)
        else:
            countdown_window.destroy() 
            action_log(player_teams) 
        
    update_countdown(-1) 
    countdown_window.mainloop()

def send_start_signal():
        # This function sends the "202" message to the traffic generator.
        import socket
        signal_message = "202"
        target_address = ("127.0.0.1", 7500)  # traffic generator's receiving address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(signal_message.encode(), target_address)
            print("Start signal '202' sent to traffic generator.")
        except Exception as e:
            print("Error sending start signal:", e)
        finally:
            sock.close()

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
    player_labels = {}

    for index, (name, _, _) in enumerate(player_teams["Red"], start=1):
        key = f"red_player{index}_score"
        player_scores[key] = 0
        label = tk.Label(left_team_frame, text=f"{name} - Score: 0", font=("Arial", 14), fg="red", bg="black")
        label.pack()
        player_labels[key] = label
    
    for index, (name, _, _) in enumerate(player_teams["Green"], start=1):
        key = f"green_player{index}_score"
        player_scores[key] = 0
        label = tk.Label(right_team_frame, text=f"{name} - Score: 0", font=("Arial", 14), fg="green", bg="black")
        label.pack()
        player_labels[key] = label

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

    timer_label = tk.Label(bottom_frame, text="Time Remaining: 6:00", font=("Arial", 16, "bold"), fg="white", bg="black")
    timer_label.pack()


    def update_timer(time_left):
        if time_left >= 0:
                minutes = time_left // 60
                seconds = time_left % 60
                timer_label.config(text=f"Time Remaining: {minutes}:{seconds:02d}")
                action_window.after(1000, update_timer, time_left - 1)
        else:
            timer_label.config(text="Times up!")


    update_timer(360)
#############################################
    # add points based on signal
    def process_signal(code, hardware_id):
        nonlocal player_scores, player_labels

        # Split signal into hardware_id and base_code
        hardware_id, base_code = code.split(":")
        base_code = base_code.strip()
        player_name = None


        # Split signal into player1_id and player2_id
        player1_id, player2_id = code.split(":")
        player1_id = player1_id.strip()
        player2_id = player2_id.strip()

        # Find players associated with player1_id and player2_id
        player1_name = None
        player2_name = None
        for team in ["Red", "Green"]:
            for player, player_hardware_id in player_teams[team]:
                if player_hardware_id == player1_id:
                    player1_name = player
                if player_hardware_id == player2_id:
                    player2_name = player
                if player1_name and player2_name:
                    break
            if player1_name and player2_name:
                break

        if not player1_name or not player2_name:
            action_log.insert(tk.END, f"Unknown hardware IDs: {player1_id}, {player2_id}\n")
            return

        # Player vs Player collision (gain 10 points)
        if player1_id != player2_id:  # Ensure it's not a self-hit
            action_log.insert(tk.END, f"Player {player1_name} hit Player {player2_name} (ID: {player1_id} -> {player2_id}) and gained 10 points!\n")
            player_scores[f"red_player{player1_id}_score"] += 10  # Example: Update red team's player 1 score
            player_scores[f"green_player{player2_id}_score"] += 10  # Example: Update green team's player 2 score

            # Update score label
            player_labels[f"red_player{player1_id}_score"].config(text=f"{player1_name} - Score: {player_scores[f'red_player{player1_id}_score']}")
            player_labels[f"green_player{player2_id}_score"].config(text=f"{player2_name} - Score: {player_scores[f'green_player{player2_id}_score']}")

        if base_code == "53":  # Red base has been scored on
            action_log.insert(tk.END, f"Red base has been hit by player {player_name} (ID: {hardware_id})\n")
            for i in range(1, len(player_teams["Green"]) + 1):
                key = f"green_player{i}_score"
                player_scores[key] += 100  # Base score
                player_labels[key].config(text=f"{player_teams['Green'][i-1][0]} - Score: {player_scores[key]}")
        elif base_code == "43":  # Green base has been scored on
            action_log.insert(tk.END, f"Green base has been hit by player {player_name} (ID: {hardware_id})\n")
            for i in range(1, len(player_teams["Red"]) + 1):
                key = f"red_player{i}_score"
                player_scores[key] += 100  # Base score
                player_labels[key].config(text=f"{player_teams['Red'][i-1][0]} - Score: {player_scores[key]}")



    ###############################
    # testing signal until using traffic generator
    

    #####################################

    # Switch back to player screen
    def on_f1(event):
        action_window.destroy()
        playerScreen.playerScreen()
    
    action_window.bind("<F1>", on_f1)

    # f1_button = tk.Button(action_window, text="Start", command=on_f1)
    # f1_button.pack(pady=20)

    action_window.mainloop()
#
