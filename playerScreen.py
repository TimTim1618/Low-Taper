from splashScreen import SplashScreen
import tkinter as tk


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

    # Function to capture and store name and equipment ID
    def store_info():
        player_name = name_entry.get()
        equipment_id = equipment_entry.get()
        #print out information to terminal
        print(f"Player Name: {player_name}, Equipment ID: {equipment_id}")

    submit_button = tk.Button(left_frame, text="Submit", command=store_info)
    submit_button.place(x=300, y=565)

    root.mainloop()
    
    root.mainloop()

def main():
    SplashScreen()
    playerScreen()


if __name__ == "__main__":
    main()
