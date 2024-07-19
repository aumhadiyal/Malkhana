import datetime
import tkinter as tk
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutFSL as cof
import MalkhanaTable.MalkhanaPage as m
import Log.log as log
from tkinter import ttk
import sqlite3
import MalkhanaTable.checkout.checkoutpage as co
from tkcalendar import DateEntry
from tkinter import messagebox
import login.login as login
import logger as lu

checkout_frame = None


def checkout_destroyer():
    if checkout_frame is not None:
        checkout_frame.destroy()


def update_item_status(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='court' where barcode = ?", (barcode,))
    con.commit()
    con.close()
    conn = sqlite3.connect("databases/court_records.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS court_records (
    barcode TEXT UNIQUE,
    fir_no TEXT UNIQUE,
    seized_items TEXT,
    checkout_date TEXT,
    checkout_time TEXT,
    taken_by_whom TEXT,
    checkin_date TEXT,
    checkin_time TEXT,
    order_details TEXT,
    entry_time TEXT
    );''')
    entry_time = datetime.datetime.now()
    cursor.execute("INSERT INTO court_records (barcode,fir_no,seized_items,checkout_date,checkout_time,taken_by_whom,entry_time) values(?,?,?,?,?,?,?)",
                   (barcode, fir_no, seized_items, checkout_date, checkout_time, taken_by_whom, entry_time))
    conn.commit()
    conn.close()
    messagebox.showinfo("Successful", "Succesfully checked out from Malkhana")
    log.update_logs(barcode, "CheckOut Into Court",
                    checkout_date, checkout_time)
    activity = "Item checked out to Court barcode no: "+barcode
    lu.log_activity(login.current_user, activity)


def checkouttocourt():
    barcode = barcode_entry.get()
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    taken_by_whom = taken_by_whom_entry.get()
    checkout_date = checkout_date_entry.get_date()
    checkout_time = f"{hour_var.get()}:{minute_var.get()}"

    barcode_checker(barcode, checkout_date, checkout_time,
                    taken_by_whom, seized_items, fir_no)

    # Clear the input fields after checkout
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)  # Clear the date entry


def checkouttofsl_page():
    global checkout_frame
    checkout_destroyer()
    cof.checkouttoFSL_page(checkout_frame)


def checkouttocourt_page(root):
    root.destroy()
    global checkout_frame, barcode_entry, fir_no_entry, seized_items_entry, taken_by_whom_entry, checkout_date_entry, hour_var, minute_var
    checkout_destroyer()
    checkout_frame = tk.Frame(root.master)
    checkout_frame.master.title("Checkout to Court")
    checkout_frame.pack(fill=tk.BOTH, expand=True)

    screen_width = checkout_frame.winfo_screenwidth()
    screen_height = checkout_frame.winfo_screenheight()

    # Sidebar
    sidebar = tk.Frame(checkout_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkout to FSL", checkouttofsl_page),
        ("Checkout to Court", None),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        if text == "Checkout to Court":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Define fonts
    textbox_font = ('Helvetica', 12)
    font_style = ('Helvetica', 12)

    # Labels and Entry Fields
    font_style = ('Helvetica', 12)

    # Labels
    tk.Label(checkout_frame, text="Barcode Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    barcode_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    barcode_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="FIR Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    fir_no_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    fir_no_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Seized Items:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    seized_items_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    seized_items_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Undertaking Inspector:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    taken_by_whom_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    taken_by_whom_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Crime Date:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    crime_date_entry = DateEntry(checkout_frame, font=textbox_font,
                                 width=12, background='darkblue', foreground='white', borderwidth=2)
    crime_date_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Crime Time:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")

    time_frame = tk.Frame(checkout_frame, bg="#f6f4f2")
    time_frame.pack(padx=10, pady=5, anchor="w")

    hour_var = tk.StringVar(time_frame, value='00')
    hour_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=hour_var, values=[
        str(i).zfill(2) for i in range(24)], state='readonly', width=5)

    minute_var = tk.StringVar(time_frame, value='00')
    minute_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=minute_var, values=[
        str(i).zfill(2) for i in range(60)], state='readonly', width=5)

    hour_menu.pack(side=tk.LEFT, pady=5)
    minute_menu.pack(side=tk.LEFT, padx=10, pady=5)

    button_font = ('Helvetica', 12)
    # Adjusted button sizes
    button_width = 20
    button_height = 2

    checkout_button = tk.Button(checkout_frame, text="Checkout Item",
                                background="#f6f4f2", command=checkouttocourt, font=button_font, width=button_width, height=button_height)
    checkout_button.pack(padx=10, side=tk.LEFT)

    # Back Button
    back_button = tk.Button(checkout_frame, text="Back",
                            background="#f6f4f2", command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Home Button
    home_button = tk.Button(checkout_frame, text="Home",
                            background="#f6f4f2", command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(padx=10, pady=5, side=tk.LEFT)


def go_back():
    checkout_destroyer()
    co.COpage(checkout_frame)


def go_home():
    checkout_destroyer()
    Homepage.open_homepage(checkout_frame)


def barcode_checker(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode not Found",
                             "Barcode doesnt exist in the database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)  # Clear the date entry
        return
    already_outornot(barcode, checkout_date, checkout_time,
                     taken_by_whom, seized_items, fir_no)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)  # Clear the date entry


def already_outornot(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("malkhana", "Malkhana"):
        update_item_status(barcode, checkout_date, checkout_time,
                           taken_by_whom, seized_items, fir_no)
    else:
        messagebox.showerror("Item not found",
                             "Item is not present in Malkhana.")
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)
