import tkinter as tk
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
import login.login as l


def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def main():
    root = tk.Tk()
    root.state('zoomed')
    root.title("Main Window")

    # Apply the custom theme with background image to the root window
    set_custom_theme(root)

    # Create a ThemedStyle instance for the root window
    style = ThemedStyle(root)

    # Set the theme to 'radiance'
    style.set_theme('radiance')

    style.configure('TButton', background='#9a9a9a')  # Change 'blue' to your desired color


    main_frame = tk.Frame(root)
    main_frame.pack()
    # Call the function from the print module
    l.initloginpage(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
