import playerScreen
import tkinter as tk

#action menu
#-----------------------------------
def player_action_main(previous_window):
    #close previous window
    previous_window.destroy()


    #currently displays black screen after both teams are filled
    action_window = tk.Tk()
    action_window.title("Player Action")
    action_window.geometry("800x600")
    action_window.configure(bg="black")

    #switch back to player Screen
    def on_f1(event):
        action_window.destroy()
        playerScreen.playerScreen()
    f1_button = tk.Button(action_window, text="Player Screen", command = on_f1)
    f1_button.pack(pady=20)

    #start button
    def on_f4(event):
        #function goes here

    #f4 start button stuff. Starts countdown and music
    f4_button = tk.Button(action_window, text="Start Countdown (f4)", command = #countdown and musci function goes here )
    f4_button.pack(pady=20)   

    action_window.bind("<F1>", on_f1)

    action_window.bind("<F4>", on_f4)
    action_window.mainloop()

    

#-----------------------------------


    #pass


