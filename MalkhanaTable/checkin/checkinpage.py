import tkinter as tk
from ttkthemes import ThemedStyle
import MalkhanaTable.checkin.checkinFromFSL as f
import MalkhanaTable.checkin.checkinFromCourt as c
import MalkhanaTable.checkin.checkinFromFSL as ci
import home.Homepage as Homepage
import MalkhanaTable.MalkhanaPage as m

CI_frame = None


def CIpage(prev_homepage_frame):
    prev_homepage_frame.destroy()
    global CI_frame
    checkin_page_destroyer()
    CI_frame = tk.Frame(prev_homepage_frame.master)
    CI_frame.master.title("Checkin")
    CI_frame.pack(fill=tk.BOTH, expand=True)

    style = ThemedStyle(CI_frame)
    style.theme_use('radiance')

    # Define button font size
    button_font = ('Helvetica', 15)

    checkinFSL = tk.Button(CI_frame, text="Checkin From FSL",
                           background="#FFFFFF", command=fsl, font=button_font, height=1, width=15)
    checkinFSL.pack(pady=20)

    checkinCourt = tk.Button(CI_frame, text="Checkin From Court",
                             background="#FFFFFF", command=court, font=button_font, height=1, width=15)
    checkinCourt.pack(pady=20)

    Home = tk.Button(CI_frame, text="Home", command=go_home,
                     background="#FFFFFF", font=button_font, height=1, width=10)
    Home.pack(padx=10, pady=10)

    back_button = tk.Button(CI_frame, text="Back", command=go_back,
                            background="#FFFFFF", font=button_font, height=1, width=10)
    back_button.pack(padx=10, pady=10)

    CI_frame.mainloop()


def go_back():
    checkin_page_destroyer()
    m.mkpage(CI_frame)


def go_home():
    checkin_page_destroyer()
    Homepage.open_homepage_r(CI_frame)


def fsl():
    checkin_page_destroyer()
    f.checkin_page(CI_frame)


def court():
    checkin_page_destroyer()
    c.checkin_page_2(CI_frame)


def checkin_page_destroyer():
    if CI_frame is not None:
        CI_frame.destroy()
