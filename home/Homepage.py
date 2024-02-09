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

homepage_frame = None


def open_homepage(prev_login_frame):
    prev_login_frame.destroy()
    global homepage_frame
    homepage_destroyer()

    homepage_frame = tk.Frame(prev_login_frame.master)
    homepage_frame.pack(fill=tk.BOTH, expand=True)

    # Apply Radiance theme
    style = ThemedStyle(homepage_frame)
    style.theme_use('radiance')

    # table_button = tk.Button(homepage_frame, text="Malkhana",
    #                          command=clicked, font=("Helvetica", 15), width=10, height=1)
    # table_button.grid(row=0, column=0, pady=25, padx=75)

    # FSL_button = tk.Button(homepage_frame, text="FSL Info",
    #                        command=fsl, font=("Helvetica", 15), width=10, height=1)
    # FSL_button.grid(row=1, column=0, pady=25, padx=75)

    # Court_button = tk.Button(homepage_frame, text="Court Info",
    #                          command=court, font=("Helvetica", 15), width=10, height=1)
    # Court_button.grid(row=2, column=0, pady=25, padx=75)

    # log_button = tk.Button(homepage_frame, text="Logs",
    #                        command=log, font=("Helvetica", 15), width=10, height=1)
    # log_button.grid(row=3, pady=25, padx=75)

    # print_button = tk.Button(homepage_frame, text="Print", command=printDetails,
    #                          font=("Helvetica", 15), width=10, height=1)
    # print_button.grid(row=4, pady=25, padx=75)

    # logout = tk.Button(homepage_frame, text="Log Out", command=logoutclicked,
    #                    font=("Helvetica", 15), width=10, height=1)
    # logout.grid(row=5, pady=25, padx=75)

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


def open_homepage_r(return_frame):
    return_frame.destroy()
    global homepage_frame

    homepage_destroyer()

    homepage_frame = tk.Frame(return_frame.master)
    homepage_frame.pack(fill=tk.BOTH, expand=True)
    homepage_frame.master.title("HomePage")
    # Apply Radiance theme
    style = ThemedStyle(homepage_frame)
    style.theme_use('radiance')

    # table_button = tk.Button(homepage_frame, text="Malkhana",
    #                          command=clicked, font=("Helvetica", 15), width=10, height=1)
    # table_button.grid(row=0, column=5, pady=25, padx=75)

    # FSL_button = tk.Button(homepage_frame, text="FSL Info",
    #                        command=fsl, font=("Helvetica", 15), width=10, height=1)
    # FSL_button.grid(row=1, column=5, pady=25, padx=75)

    # Court_button = tk.Button(homepage_frame, text="Court Info",
    #                          command=court, font=("Helvetica", 15), width=10, height=1)
    # Court_button.grid(row=2, column=5, pady=25, padx=75)

    # log_button = tk.Button(homepage_frame, text="Logs",
    #                        command=log, font=("Helvetica", 15), width=10, height=1)
    # log_button.grid(row=3, pady=25, padx=75)

    # print_button = tk.Button(homepage_frame, text="Print", command=printDetails,
    #                          font=("Helvetica", 15), width=10, height=1)
    # print_button.grid(row=4, pady=25, padx=75)

    # logout = tk.Button(homepage_frame, text="Log Out", command=logoutclicked,
    #                    font=("Helvetica", 15), width=10, height=1)
    # logout.grid(row=5, pady=25, padx=75)

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
