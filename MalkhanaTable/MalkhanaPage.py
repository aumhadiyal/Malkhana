import tkinter as tk
from ttkthemes import ThemedStyle
import MalkhanaTable.additems.additems as a
import MalkhanaTable.checkout.checkoutpage as co
import MalkhanaTable.checkin.checkinpage as ci
import home.Homepage as Homepage
import MalkhanaTable.viewitems.viewitems as v
import login.login as login
from PIL import Image, ImageTk

malkhanapage_frame = None


def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def mkpage(prev_homepage_frame):
    prev_homepage_frame.destroy()

    global malkhanapage_frame
    malkhana_destroyer()
    malkhanapage_frame = tk.Frame(prev_homepage_frame.master)
    malkhanapage_frame.master.title("Malkhana page")
    malkhanapage_frame.pack(fill=tk.BOTH, expand=True)

     # Get screen width and height
    screen_width = malkhanapage_frame.winfo_screenwidth()
    screen_height = malkhanapage_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(malkhanapage_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Apply Radiance theme
    style = ThemedStyle(malkhanapage_frame)
    style.theme_use('radiance')

    # Menu Buttons
    buttons = [
        ("Add Items", additemsclicked),
        ("View Items", viewitemsclicked),
        ("Checkout Items", checkoutclicked),
        ("Checkin Items", checkinclicked),
        ("Back ", go_back),
        ("Log Out", logoutclicked),
    ]

    for text, command in buttons:
        button = tk.Button(malkhanapage_frame, text=text,
                           background=style.lookup('TButton', 'background'), command=command, font=("Helvetica", 15), width=15, height=1)
        button.pack(pady=10)

    malkhanapage_frame.mainloop()


def go_back():
    malkhana_destroyer()
    Homepage.open_homepage(malkhanapage_frame)


def logoutclicked():
    malkhana_destroyer()
    login.initloginpage(malkhanapage_frame)


def additemsclicked():
    malkhana_destroyer()
    a.additems(malkhanapage_frame)


def checkinclicked():
    malkhana_destroyer()
    ci.CIpage(malkhanapage_frame)


def checkoutclicked():
    malkhana_destroyer()
    co.COpage(malkhanapage_frame)


def viewitemsclicked():
    malkhana_destroyer()
    v.viewitems(malkhanapage_frame)


def malkhana_destroyer():
    if malkhanapage_frame is not None:
        malkhanapage_frame.destroy()
