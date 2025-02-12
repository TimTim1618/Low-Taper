import playerScreen
import tkinter as tk
#action menu
#-----------------------------------
def player_action_main(previous_window):
    #close previous window
    previous_window.destroy()


    #currently displays black screen after both teams are filled
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Player Action Screen")
    root.configure(bg="black")


    root.mainloop()



    #pass


