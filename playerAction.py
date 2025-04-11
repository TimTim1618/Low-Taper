import playerScreen
from networkSelector import UdpTransmitter
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import pygame
import os
import random
import threading
import socket
import logging
import sys



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
    #     print(f"Now playing: {os.path.basename(track_path)}")\

       

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
            # commented out for now with hello statement
                # play_track(sound_files[0])
                 print("hello")
             countdown_label.config(image=countdown_images[index])
             countdown_window.after(1000, update_countdown, index + 1)
         elif index < len(countdown_images):
             countdown_label.config(image=countdown_images[index])
             countdown_window.after(1000, update_countdown, index + 1)
         else:
             # send "202" start signal to traffic generator
             countdown_window.destroy()
             action_log(player_teams) 
 

    update_countdown(-1)
    countdown_window.mainloop()


def action_log(player_teams):
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

    player_scores = {}
    player_labels = {}
    hardware_to_key = {}
    has_b = {}

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

#------------------------------------------------------------------------------
    def send_end_signal():
        def send_once(i):
            signal_message = "221"
            target_address = ("127.0.0.1", 7500)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.sendto(signal_message.encode(), target_address)
                print(f"Sent end signal '221' ({i+1}/3)")
            except Exception as e:
                print(f"Error sending end signal: {e}")
            finally:
                sock.close()

        for i in range(3):
            action_window.after(i * 200, lambda i=i: send_once(i))

# -------------------------------------------------------------------------

    def update_timer(time_left):
        if time_left >= 0:
            minutes = time_left // 60
            seconds = time_left % 60
            timer_label.config(text=f"Time Remaining: {minutes}:{seconds:02d}")
            action_window.after(1000, update_timer, time_left - 1)
        else:
            timer_label.config(text="Times up!")
            send_end_signal()

    update_timer(360)

    def on_f1(event):
        # Set a flag to stop the listener thread
        global listener_running
        listener_running = False
        action_window.destroy()
        playerScreen.playerScreen()

    action_window.bind("<F1>", on_f1)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#--------------------------------------------------------------------------------------------#

    def get_name_from_id(hardware_id, player_teams):
            for team in ["Red", "Green"]:
                for name, h_id, _ in player_teams[team]:
                   # print(f"Comparing: {str(hardware_id)} == {str(h_id)}")
                    if str(h_id) == str(hardware_id):
                        return name
            return "Unknown"
#--------------------------------------------------------------------------------------------#
                    # connections #

    def send_start_signal():
        import socket
        import time

        signal_message = "202"
        target_address = ("127.0.0.1", 7500)  # traffic generator receiving address

        # Send signal
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(signal_message.encode(), target_address)
            print("Start signal '202' sent to traffic generator.")
        except Exception as e:
            print(f"Error sending start signal: {e}")
        finally:
            sock.close()

            #after 6 minutes do this function
            #implement this later

    
    def process_signal(message):
        print("Signal received:", message)
        try:
            if ":" in message:
                parts = message.strip().split(":")
                if len(parts) == 2:
                    id1, id2 = parts

                    # Base hit logic
                    if id2 in ("53", "43"):
                        team_hit = "Red" if id2 == "53" else "Green"
                        team_awarded = "Green" if team_hit == "Red" else "Red"
                        hitter_name = get_name_from_id(id1, player_teams)

                        action_log_text.insert(tk.END, f"{team_hit} base has been hit by {hitter_name}\n")
                        action_log_text.see(tk.END)

                        for i, (name, h_id, _) in enumerate(player_teams[team_awarded], start=1):
                            if str(h_id) == str(id1):
                                key = f"{team_awarded.lower()}_player{i}_score"
                                player_scores[key] += 100
                                # add B next to name
                                 
                                if str(h_id) not in has_b:
                                    has_b[str(h_id)] = True
                                    display_name = f"{name} 🅱"
                                else:
                                    display_name = name if name.endswith( " 🅱") else f"{name} 🅱" 

                                player_labels[key].config(text=f"{display_name} - Score: {player_scores[key]}")
                                break

                    # Player hit logic
                    else:
                        shooter_name = get_name_from_id(id1, player_teams)
                        target_name = get_name_from_id(id2, player_teams)
                        action_log_text.insert(tk.END, f"{shooter_name} HAS BLASTED {target_name} WITH THEIR PHOTON BLASTER\n")
                        action_log_text.see(tk.END)

                        #reward shooter
                        for team in ["Red", "Green"]:
                            for i, (name, h_id, _) in enumerate(player_teams[team], start=1):
                                if str(h_id) == str(id1):
                                    key = f"{team.lower()}_player{i}_score"
                                    player_scores[key] += 10
                                    # preserve B if its already been awarded
                                    if has_b.get(str(id1)):
                                        display_name = f"{name } 🅱"
                                    else:
                                        display_name = name
                                    player_labels[key].config(text=f"{display_name} - Score: {player_scores[key]}")
        except Exception as e:
            print("Error processing signal:", e)


    def listen_for_signal(process_signal):
        import socket
        import logging
      
        localIP = "127.0.0.1"
        localPort = 7501

        logging.info(f"Starting UDP listener on {localIP}:{localPort}")
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            UDPServerSocket.bind((localIP, localPort))
            logging.info("Start UDP listener thread...")
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

                    process_signal(message)

                    # Define the response before sending it
                    response_message = f"Received: {message}"

                    #send a reply back to server
                    reply_ip = address[0]
                    reply_port = 7500
                    UDPServerSocket.sendto(response_message.encode(), (reply_ip, reply_port))
                    logging.info(f"Sending response to {reply_ip}:{reply_port}")

                except socket.timeout:
                    pass  # Prevents freezing when there's no incoming message

                except socket.error as e:
                    logging.warning(f"Error receiving data: {e}")

        except KeyboardInterrupt:
            logging.info("Server shutting down.")
        finally:
            UDPServerSocket.close()

#--------------------------------------------------------------------------------#

    global listener_running
    listener_running = False
    listener_thread = threading.Thread(target=send_start_signal, daemon=True)
    listener_thread.start()

    listener_thread_2 = threading.Thread(target=listen_for_signal, args=(process_signal,), daemon=True)
    listener_thread_2.start()


    def on_closing():
        global listener_running
        listener_running = False
        action_window.destroy()

    action_window.protocol("WM_DELETE_WINDOW", on_closing)

    action_window.mainloop()