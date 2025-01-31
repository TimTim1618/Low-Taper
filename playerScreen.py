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

    entry_label = tk.Label(left_frame, text="Enter your name:", bg = "red", fg = "white")
    entry_label.place(x = 10, y = 550)

    entry = tk.Entry(left_frame)
    entry.place(x = 120, y = 550)

    root.mainloop()


def main():
    SplashScreen()
    playerScreen()


if __name__ == "__main__":
    main()
