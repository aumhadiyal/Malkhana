import tkinter as tk
from PIL import Image,ImageTk
from ttkthemes import ThemedStyle
import MalkhanaTable.additems.additems as a
import home.Homepage as Homepage
import Log.log as log
import MalkhanaTable.checkin.checkinpage as cp
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox
import login.login as login
import logger as lu
checkin_frame = None


def update_item_status(barcode, checkin_date, checkin_time, order_details):
    conn = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET item_status='malkhana' where barcode = ?", (barcode,))
    conn.commit()
    conn.close()
    conn = sqlite3.connect("databases/court_records.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE court_records SET checkin_date = ?,checkin_time=?,order_details=? WHERE barcode = ?",
                   (checkin_date, checkin_time, order_details, barcode))
    barcode_entry.delete(0, tk.END)
    order_details_entry.delete("1.0", "end-1c")
    conn.commit()
    conn.close()
    messagebox.showinfo("Successful", "Succesfully entered into Malkhana")
    log.update_logs(barcode, "Checkin From Court",
                    checkin_date, checkin_time)
    activity = "Item checked in from Court barcode no: "+barcode
    lu.log_activity(login.current_user, activity)


def checkin():
    barcode = barcode_entry.get()
    checkin_time = f"{hour_var.get()}:{minute_var.get()}"
    checkin_date = checkin_date_entry.get_date()
    order_details = order_details_entry.get("1.0", "end-1c")

    barcode_checker(barcode, checkin_date, checkin_time, order_details)

    # Clear the input fields after check-in
    barcode_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)  # Clear the date entry
    order_details_entry.delete("1.0", tk.END)


def checkin_page_2(root):
    global checkin_frame, barcode_entry, checkin_date_entry, hour_var, minute_var, order_details_entry
    checkin_frame = tk.Frame(root.master)
    checkin_frame.master.title("Checkin From Court")

     # Get screen width and height
    screen_width = checkin_frame.winfo_screenwidth()
    screen_height = checkin_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(checkin_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Use pack for the checkin_frame
    checkin_frame.pack(fill=tk.BOTH, expand=True)


    style = ThemedStyle(checkin_frame)
    style.theme_use('radiance')
    # Labels
    label_barcode = tk.Label(
        checkin_frame, text="Barcode No:", background="#fff1f1",   font=("Helvetica", 12))
    label_checkin_time = tk.Label(
        checkin_frame, text="Checkin Time:", background="#fff1f1",  font=("Helvetica", 12))
    label_checkin_date = tk.Label(
        checkin_frame, text="Checkin Date:", background="#fff1f1",  font=("Helvetica", 12))
    label_order_details = tk.Label(
        checkin_frame, text="Order Details:",  background="#fff1f1", font=("Helvetica", 12))

    label_barcode.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    label_checkin_time.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    label_checkin_date.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    label_order_details.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    # Entry fields
    barcode_entry = ttk.Entry(checkin_frame, width=30, font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    barcode_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    hour_var = tk.StringVar(checkin_frame, value='00')
    minute_var = tk.StringVar(checkin_frame, value='00')

    hour_menu = ttk.Combobox(checkin_frame, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)],
                             state='readonly', width=5)
    minute_menu = ttk.Combobox(checkin_frame, textvariable=minute_var, values=[str(i).zfill(2) for i in range(60)],
                               state='readonly', width=5)
    hour_menu.grid(row=1,  column=1, padx=10, pady=10, sticky="w")
    minute_menu.grid(row=1,  column=1, padx=(10, 150), pady=10, sticky="e")

    # Date field using tkcalendar
    checkin_date_entry = DateEntry(
        checkin_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    # Use sticky=tk.W for left alignment
    checkin_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    # Text area for order details
    order_details_entry = tk.Text(
        checkin_frame, height=5, width=30, background="#FFFFFF", font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    order_details_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    # Check-in button
    checkin_button = tk.Button(checkin_frame, text="Checkin",
                               command=checkin,  background="#9a9a9a", font=("Helvetica", 12))
    checkin_button.grid(row=4, column=0, columnspan=4,
                        padx=10, pady=10, sticky="ew")

    button_font = ('Helvetica', 12)
    back_button = tk.Button(checkin_frame, text="Back",
                            background="#9a9a9a", command=go_back, font=button_font)
    back_button.grid(row=0, column=30, padx=10, pady=10, sticky="w")

    home_button = tk.Button(checkin_frame, text="Home",
                            background="#9a9a9a", command=go_home, font=button_font)
    home_button.grid(row=0, column=31, padx=10, pady=10, sticky="w")


def go_home():
    checkin_destroyer()
    Homepage.open_homepage(checkin_frame)


def go_back():
    checkin_destroyer()
    cp.CIpage(checkin_frame)


def checkin_destroyer():
    if checkin_frame is not None:
        checkin_frame.destroy()


def barcode_checker(barcode, checkin_date, checkin_time, order_details):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found",
                             "Barcode Entered Is Not Found In The Database.")
        barcode_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)  # Clear the date entry
        order_details_entry.delete("1.0", tk.END)
        return
    already_in_or_not(barcode, checkin_date, checkin_time, order_details)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)  # Clear the date entry
    order_details_entry.delete("1.0", tk.END)


def already_in_or_not(barcode, checkin_date, checkin_time, order_details):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("court", "Court"):
        update_item_status(barcode, checkin_date, checkin_time, order_details)
    else:
        messagebox.showerror("Item Exists In Malkhana/FSL",
                             "Item Already Exists In Malkhana/FSL.")
        barcode_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)  # Clear the date entry
        order_details_entry.delete("1.0", tk.END)
