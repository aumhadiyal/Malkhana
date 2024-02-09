import tkinter as tk
from ttkthemes import ThemedStyle
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutCourt as c
import MalkhanaTable.checkout.checkoutFSL as f
import MalkhanaTable.MalkhanaPage as m

CO_frame = None


def COpage(prev_CO_frame):
    prev_CO_frame.destroy()
    global CO_frame
    checkout_page_destroyer()
    CO_frame = tk.Frame(prev_CO_frame.master)
    CO_frame.master.title("Check Out ")
    CO_frame.pack(fill=tk.BOTH, expand=True)

    # Apply Radiance theme
    style = ThemedStyle(CO_frame)
    style.theme_use('radiance')

    buttons = [
        ("Checkout to FSL", fsl),
        ("Checkout to Court", court),
        ("Home", go_home),
        ("Back", go_back)]

    for text, command in buttons:
        button = tk.Button(CO_frame, text=text,
                           background=style.lookup('TButton', 'background'), command=command, font=("Helvetica", 15), width=15, height=1)
        button.pack(pady=10)

    CO_frame.mainloop()


def go_back():
    checkout_page_destroyer()
    m.mkpage(CO_frame)


def go_home():
    checkout_page_destroyer()
    Homepage.open_homepage(CO_frame)


def fsl():
    checkout_page_destroyer()
    f.checkouttoFSL_page(CO_frame)


def court():
    checkout_page_destroyer()
    c.checkouttocourt_page(CO_frame)


def checkout_page_destroyer():
    if CO_frame is not None:
        CO_frame.destroy()
