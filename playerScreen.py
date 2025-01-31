from splashScreen import SplashScreen
import tkinter as tk


def playerScreen():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Player Screen")


    left_frame = tk.Frame(root, bg='red', width=400, height=600)
    left_frame.pack(side='left', fill='both', expand=True)

    right_frame = tk.Frame(root, bg='green', width=400, height=600)
    right_frame.pack(side='right', fill='both', expand=True)

    entry_label = tk.Label(left_frame, text="Enter your name:")
    entry_label.place(relx = 0.5, rely= 0.45, anchor = "center")

    entry = tk.Entry(root)
    entry.place(relx = 0.5, rely= 0.5, anchor = "center")

    root.mainloop()


def main():
    SplashScreen()
    playerScreen()


if __name__ == "__main__":
    main()
