import tkinter as tk
from ttkthemes import ThemedStyle
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutCourt as c
import MalkhanaTable.checkout.checkoutFSL as f
import MalkhanaTable.MalkhanaPage as m

CO_frame = None


def COpage(prev_homepage_frame):
    prev_homepage_frame.destroy()
    global CO_frame
    checkout_page_destroyer()
    CO_frame = tk.Frame(prev_homepage_frame.master)
    CO_frame.master.title("Check Out ")
    CO_frame.pack(fill=tk.BOTH, expand=True)

    # Apply Radiance theme
    style = ThemedStyle(CO_frame)
    style.theme_use('radiance')

    # Create container frame
    container_frame = tk.Frame(
        CO_frame, background=style.lookup('TFrame', 'background'))
    container_frame.pack(padx=20, pady=20)

    # Checkout buttons
    checkoutFSL = tk.Button(container_frame, text="Checkout to FSL",
                            command=fsl, font=("Helvetica", 15), width=15, height=1)
    checkoutFSL.grid(row=0, column=0, pady=20)

    checkoutCourt = tk.Button(container_frame, text="Checkout to Court",
                              command=court, font=("Helvetica", 15), width=15, height=1)
    checkoutCourt.grid(row=1, column=0, pady=20)

    # Navigation buttons
    Home = tk.Button(container_frame, text="Home", command=go_home,
                     font=("Helvetica", 15), width=10, height=1)
    Home.grid(row=2, column=0, padx=10, pady=[20,])

    back_button = tk.Button(container_frame, text="Back", command=go_back,
                            font=("Helvetica", 15), width=10, height=1)
    back_button.grid(row=3, column=0, padx=10, pady=10)

    CO_frame.mainloop()


def go_back():
    checkout_page_destroyer()
    m.mkpage(CO_frame)


def go_home():
    checkout_page_destroyer()
    Homepage.open_homepage_r(CO_frame)


def fsl():
    checkout_page_destroyer()
    f.checkouttoFSL_page(CO_frame)


def court():
    checkout_page_destroyer()
    c.checkouttocourt_page(CO_frame)


def checkout_page_destroyer():
    if CO_frame is not None:
        CO_frame.destroy()
