import datetime
import tkinter as tk

from ttkthemes import ThemedStyle
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutpage as cof
import MalkhanaTable.MalkhanaPage as m
import Log.log as log
from tkinter import ttk
import sqlite3
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


def checkouttocourt_page(root):
    root.destroy()
    global checkout_frame, barcode_entry, fir_no_entry, seized_items_entry, taken_by_whom_entry, checkout_date_entry, hour_var, minute_var
    checkout_destroyer()
    checkout_frame = tk.Frame(root.master)
    checkout_frame.master.title("Checkout to Court")
    checkout_frame.pack(fill=tk.BOTH, expand=True)

    # Apply Radiance theme
    style = ThemedStyle(checkout_frame)
    style.theme_use('radiance')

    # Define layout parameters
    label_layout = {
        "padx": 10,
        "pady": 10,
        "sticky": tk.W
    }
    entry_layout = {
        "padx": 10,
        "pady": 10,
        "sticky": tk.W
    }
    button_layout = {
        "padx": 10,
        "pady": 10,
        "sticky": "ew"
    }

    # Labels
    tk.Label(checkout_frame, text="Barcode :", background="#fff1f1", font=("Helvetica", 12)).grid(
        row=0, column=0, **label_layout)
    tk.Label(checkout_frame, text="FIR No:", background="#fff1f1", font=("Helvetica", 12)).grid(
        row=1, column=0, **label_layout)
    tk.Label(checkout_frame, text="Seized Items:", background="#fff1f1", font=("Helvetica", 12)).grid(
        row=2, column=0, **label_layout)
    tk.Label(checkout_frame, text="Undertaking Officer :", background="#fff1f1", font=("Helvetica", 12)).grid(
        row=3, column=0, **label_layout)
    tk.Label(checkout_frame, text="Checkout Date:",  background="#fff1f1", font=("Helvetica", 12)).grid(
        row=4, column=0, **label_layout)
    tk.Label(checkout_frame, text="Checkout Time:", background="#fff1f1", font=("Helvetica", 12)).grid(
        row=5, column=0, **label_layout)

    # Entry fields
    barcode_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    fir_no_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    seized_items_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    taken_by_whom_entry = ttk.Entry(checkout_frame, font=("Helvetica", 12))
    barcode_entry.grid(row=0, column=1, **entry_layout)
    fir_no_entry.grid(row=1, column=1, **entry_layout)
    seized_items_entry.grid(row=2, column=1, **entry_layout)
    taken_by_whom_entry.grid(row=3, column=1, **entry_layout)

    # Comboboxes for time
    hour_var = tk.StringVar(checkout_frame, value='00')
    minute_var = tk.StringVar(checkout_frame, value='00')
    hour_menu = ttk.Combobox(checkout_frame, textvariable=hour_var, values=[
                             str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_menu = ttk.Combobox(checkout_frame, textvariable=minute_var, values=[
                               str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    hour_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")
    minute_menu.grid(row=5,  column=1, padx=10, pady=10, sticky="e")

    # Date field using tkcalendar
    checkout_date_entry = DateEntry(
        checkout_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkout_date_entry.grid(row=4, column=1, **entry_layout)

    # Checkout button
    checkout_button = tk.Button(checkout_frame, text="Checkout to Court",
                                background="#FFFFFF", command=checkouttocourt, font=("Helvetica", 12))
    checkout_button.grid(row=6, column=0, columnspan=4,
                         **button_layout)

    # Buttons for navigation
    button_font = ('Helvetica', 12)
    back_button = tk.Button(checkout_frame, text="Back",
                            background="#FFFFFF", command=go_back, font=button_font)
    back_button.grid(row=0, column=30, **label_layout)

    home_button = tk.Button(checkout_frame, text="Home",
                            background="#FFFFFF", command=go_home, font=button_font)
    home_button.grid(row=0, column=31, **label_layout)


def go_back():
    checkout_destroyer()
    cof.COpage(checkout_frame)


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
