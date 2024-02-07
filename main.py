import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import login.logindb as ll
import login.login as login


def set_custom_theme(root):
    root.tk_setPalette(background="#B9E6FF", foreground="black",
                       activeBackground="#D3D3D3", activeForeground="black")
    root.option_add("*TEntry*background", "white")
    root.option_add("*TEntry*foreground", "black")
    root.option_add("*TEntry*selectBackground", "#B0E0E6")
    root.option_add("*TEntry*selectForeground", "black")
    root.option_add("*TEntry*insertBackground", "black")
    # Change the button color to white
    root.option_add("*TButton*background", "white")
    # Change the button text color to white
    root.option_add("*TButton*foreground", "white")
    # Slightly lighter blue for active buttons
    root.option_add("*TButton*activeBackground", "#EBF1F1")
    root.option_add("*TButton*activeForeground", "white")

    # Set a new color for the login button (already set to #EBF1F1 in the original code)
    # Light green color for login button
    root.option_add("*TButton.login.TButton*background", "#EBF1F1")

    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize(
        (root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def main():
    root = tk.Tk()
    root.state('zoomed')
    root.title("Main Window")

    # Apply the custom theme with background image
    set_custom_theme(root)

    main_frame = tk.Frame(root)
    main_frame.pack()

    login.initloginpage(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
