import tkinter as tk
from ttkthemes import ThemedStyle
import MalkhanaTable.checkin.checkinFromFSL as f
import MalkhanaTable.checkin.checkinFromCourt as c
import MalkhanaTable.checkin.checkinFromFSL as ci
import home.Homepage as Homepage
import MalkhanaTable.MalkhanaPage as m
from PIL import Image,ImageTk

CI_frame = None


def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def CIpage(prev_homepage_frame):
    prev_homepage_frame.destroy()
    global CI_frame
    checkin_page_destroyer()
    CI_frame = tk.Frame(prev_homepage_frame.master)
    CI_frame.master.title("Checkin")
    CI_frame.pack(fill=tk.BOTH, expand=True)

         # Get screen width and height
    screen_width = CI_frame.winfo_screenwidth()
    screen_height = CI_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(CI_frame
                        , image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    style = ThemedStyle(CI_frame)
    style.theme_use('radiance')

    # Define button font size
    button_font = ('Helvetica', 15)

    checkinFSL = tk.Button(CI_frame, text="Checkin From FSL",
                           background="#FFFFFF", command=fsl, font=button_font, height=1, width=18)
    checkinFSL.pack(pady=20)

    checkinCourt = tk.Button(CI_frame, text="Checkin From Court",
                             background="#FFFFFF", command=court, font=button_font, height=1, width=18)
    checkinCourt.pack(pady=20)

    Home = tk.Button(CI_frame, text="Home", command=go_home,
                     background="#FFFFFF", font=button_font, height=1, width=13)
    Home.pack(padx=10, pady=10)

    back_button = tk.Button(CI_frame, text="Back", command=go_back,
                            background="#FFFFFF", font=button_font, height=1, width=13)
    back_button.pack(padx=10, pady=10)

    CI_frame.mainloop()


def go_back():
    checkin_page_destroyer()
    m.mkpage(CI_frame)


def go_home():
    checkin_page_destroyer()
    Homepage.open_homepage(CI_frame)


def fsl():
    checkin_page_destroyer()
    f.checkin_page(CI_frame)


def court():
    checkin_page_destroyer()
    c.checkin_page_2(CI_frame)


def checkin_page_destroyer():
    if CI_frame is not None:
        CI_frame.destroy()
