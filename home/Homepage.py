import tkinter as tk
from ttkthemes import ThemedStyle
import login.login as login
import MalkhanaTable.MalkhanaPage as mk
import FSLInfo.FSLpage as fp
import CourtInfo.Courtpage as cp
import Log.log as l
import login.login as lu
import logger
import print
from PIL import Image, ImageTk

homepage_frame = None


def open_homepage(prev_login_frame):
    prev_login_frame.destroy()
    global homepage_frame
    homepage_destroyer()

    homepage_frame = tk.Frame(prev_login_frame.master)
    homepage_frame.pack(fill=tk.BOTH, expand=True)

    # Get screen width and height
    screen_width = homepage_frame.winfo_screenwidth()
    screen_height = homepage_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(homepage_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Apply Radiance theme
    style = ThemedStyle(homepage_frame)
    style.theme_use('radiance')

    homepage_frame.master.title("HomePage")
    buttons = [
        ("Malkhana Info", clicked),
        ("FSL Info", fsl),
        ("Court Info", court),
        ("Logs", log),
        ("Print", printDetails),
        ("Log Out", logoutclicked),
    ]

    for text, command in buttons:
        button = tk.Button(homepage_frame, text=text,
                           background=style.lookup('TButton', 'background'), command=command, font=("Helvetica", 15), width=15, height=1)
        button.pack(pady=10)

    homepage_frame.mainloop()


def homepage_destroyer():
    global homepage_frame
    if homepage_frame is not None:
        homepage_frame.destroy()


def logoutclicked():
    logger.log_activity(lu.current_user, "LOG-OUT")
    homepage_destroyer()
    login.initloginpage(homepage_frame)


def clicked():
    homepage_destroyer()
    mk.mkpage(homepage_frame)


def fsl():
    homepage_destroyer()
    fp.viewfsl(homepage_frame)


def court():
    homepage_destroyer()
    cp.view_court(homepage_frame)


def log():
    homepage_destroyer()
    l.create_logs_page(homepage_frame)


def printDetails():
    homepage_destroyer()
    print.printPage(homepage_frame)
