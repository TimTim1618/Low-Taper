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


    action_window.bind("<F1>", on_f1)

    action_window.mainloop()

#-----------------------------------


    #pass


