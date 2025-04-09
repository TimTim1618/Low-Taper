import playerScreen
from networkSelector import UdpTransmitter
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import pygame
import os
import time
import random
import threading
import socket
import logging

def player_action_main(previous_window, player_teams):
    previous_window.destroy()
    countdown_timer(player_teams)

def countdown_timer(player_teams):
    countdown_window = tk.Tk()
    countdown_window.title("Countdown")
    countdown_window.geometry("800x600")
    countdown_window.configure(bg="black")

    countdown_label = Label(countdown_window, bg="black")
    countdown_label.pack(expand=True)

    image_folder = "countdown_images"
    background_path = os.path.join(image_folder, "background.tif")
    background = Image.open(background_path) if os.path.exists(background_path) else None

    alert_path = os.path.join(image_folder, "alert-on.tif")
    alert_img = Image.open(alert_path).resize((800, 600)) if os.path.exists(alert_path) else None
    alert_img = ImageTk.PhotoImage(alert_img) if alert_img else None

    countdown_images = []
    for i in range(1, -1, -1):
        num_path = os.path.join(image_folder, f"{i}.tif")
        if background and os.path.exists(num_path):
            num_img = Image.open(num_path).convert("RGBA").resize((100, 100))
            combined = background.copy().convert("RGBA")
            position = ((combined.width - num_img.width) // 2, ((combined.height - num_img.height) // 2) + 50)
            combined.paste(num_img, position, num_img)
            countdown_images.append(ImageTk.PhotoImage(combined))

    #####################################
    # commented out until timer set back to 30 seconds
    # def play_track(track_path):
    #     pygame.mixer.music.load(track_path)
    #     pygame.mixer.play()
    #     print(f"Now playing: {os.path.basename(track_path)}")

    def update_countdown(index):
         if index == -1 and alert_img:
             countdown_label.config(image=alert_img)
             countdown_window.after(1000, update_countdown, 0)
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
    signal_message = "202"
    target_address = ("127.0.0.1", 7500)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.sendto(signal_message.encode(), target_address)
            print("Start signal '202' sent to traffic generator.")
        except Exception as e:
            print("Error sending start signal:", e)

def listen_for_signal(process_signal):
    listen_address = ("127.0.0.1", 7501)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.bind(listen_address)
            print(f"Listening for signals on {listen_address[0]}:{listen_address[1]}")
            
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    message = data.decode('utf-8')
                    print(f"Received: {message} from {addr}")
                    
                    # Pass the message to the process_signal function
                    process_signal(message)
                except Exception as e:
                    print(f"Error receiving data: {e}")
        except Exception as e:
            print(f"Socket binding error: {e}")

def action_log(player_teams):
    action_window = tk.Tk()
    action_window.title("Player Action")
    action_window.geometry("800x600")
    action_window.configure(bg="black")

    transmitter = UdpTransmitter()

    top_frame = tk.Frame(action_window, bg='black')
    top_frame.pack(fill="x", padx=10, pady=5)

    left_team_frame = tk.Frame(top_frame, bg='black')
    left_team_frame.pack(side='left', expand=True)
    right_team_frame = tk.Frame(top_frame, bg='black')
    right_team_frame.pack(side='right', expand=True)

    tk.Label(left_team_frame, text="RED TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()
    tk.Label(right_team_frame, text="GREEN TEAM", font=("Arial", 18, "bold"), fg="white", bg="black").pack()

    player_scores = {}
    player_labels = {}
    hardware_to_key = {}

    for index, (name, hardware_id, _) in enumerate(player_teams["Red"], start=1):
        key = f"red_player{index}_score"
        player_scores[key] = 0
        label = tk.Label(left_team_frame, text=f"{name} - Score: 0", font=("Arial", 14), fg="red", bg="black")
        label.pack()
        player_labels[key] = label
        hardware_to_key[hardware_id] = key

    for index, (name, hardware_id, _) in enumerate(player_teams["Green"], start=1):
        key = f"green_player{index}_score"
        player_scores[key] = 0
        label = tk.Label(right_team_frame, text=f"{name} - Score: 0", font=("Arial", 14), fg="green", bg="black")
        label.pack()
        player_labels[key] = label
        hardware_to_key[hardware_id] = key

    middle_frame = tk.Frame(action_window, bg='black', highlightbackground="yellow", highlightthickness=2)
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(middle_frame, text="Current Game Action", font=("Arial", 14, "bold"), fg="white", bg="black").pack()

    action_log_frame = tk.Frame(middle_frame, bg="black")
    action_log_frame.pack(fill="both", expand=True)

    action_log_text = tk.Text(action_log_frame, height=10, bg="blue", fg="white", font=("Arial", 12, "italic"), wrap="word")
    action_log_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(action_log_frame, command=action_log_text.yview)
    scrollbar.pack(side="right", fill="y")
    action_log_text.config(yscrollcommand=scrollbar.set)

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

    def on_f1(event):
        action_window.destroy()
        playerScreen.playerScreen()

    action_window.bind("<F1>", on_f1)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def process_signal(message):
        print("Signal received:", message)
        try:
            if ":" in message:
                parts = message.strip().split(":")
                if len(parts) == 2:
                    hardware_id, base_code = parts
                    
                    if base_code in ("53", "43"):  # base hit
                        team_hit = "Red" if base_code == "53" else "Green"
                        team_awarded = "Green" if team_hit == "Red" else "Red"
                        action_log_text.insert(tk.END, f"{team_hit} base has been hit by {hardware_id}\n")
                        action_log_text.see(tk.END)
                        
                        for i, (name, h_id, _) in enumerate(player_teams[team_awarded], start=1):
                            key = f"{team_awarded.lower()}_player{i}_score"
                            player_scores[key] += 100
                            player_labels[key].config(text=f"{name} - Score: {player_scores[key]}")
                    else:  # player vs player hit
                        player1_id, player2_id = parts
                        if player1_id != player2_id:
                            key1 = hardware_to_key.get(player1_id)
                            key2 = hardware_to_key.get(player2_id)

                            if key1 and key2:
                                player_scores[key1] += 10
                                player_scores[key2] += 10
                                player_labels[key1].config(text=f"{get_name_from_id(player1_id)} - Score: {player_scores[key1]}")
                                player_labels[key2].config(text=f"{get_name_from_id(player2_id)} - Score: {player_scores[key2]}")
                                action_log_text.insert(tk.END, f"{get_name_from_id(player1_id)} hit {get_name_from_id(player2_id)}. +10 each\n")
                                action_log_text.see(tk.END)
                            else:
                                action_log_text.insert(tk.END, f"Unknown players: {player1_id}, {player2_id}\n")
                                action_log_text.see(tk.END)
                else:
                    action_log_text.insert(tk.END, f"Invalid message format: {message}\n")
                    action_log_text.see(tk.END)
            else:
                action_log_text.insert(tk.END, f"Malformed signal: {message}\n")
                action_log_text.see(tk.END)
        except Exception as e:
            action_log_text.insert(tk.END, f"Error processing signal: {e}\n")
            action_log_text.see(tk.END)

    def get_name_from_id(hardware_id):
        for team in ["Red", "Green"]:
            for name, h_id, _ in player_teams[team]:
                if h_id == hardware_id:
                    return name
        return "Unknown"
    
    listen_thread = threading.Thread(target=listen_for_signal, args=(process_signal,))
    listen_thread.daemon = True  # Make thread exit when main program exits
    listen_thread.start()
    
    action_window.mainloop()