import tkinter as tk
from PIL import Image, ImageTk

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")

        img = Image.open("logo.jpg")
        img = img.resize((800, 600), Image.Resampling.LANCZOS) 

        self.bg = ImageTk.PhotoImage(img)

        self.label = tk.Label(self.root, image = self.bg)
        self.label.place(x = 0, y = 0)

        #close after 3 seconds

        self.root.after(3000, self.root.destroy)

        self.root.mainloop()


if __name__ == "__main__":
    SplashScreen()

