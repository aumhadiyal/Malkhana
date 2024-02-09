import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
import home.Homepage as Homepage
import MalkhanaTable.MalkhanaPage as m
import login.login as login
from tkinter import filedialog
import datetime
import logger as lu
additems_frame = None

file_path = None


def additems(prev_malkhana_frame):
    prev_malkhana_frame.destroy()

    global additems_frame
    global barcode_entry, fir_no_entry, seized_items_entry, ipc_section_entry, crime_location_entry, crime_date_entry, hour_var, minute_var, crime_witness_entry, crime_inspector_entry, where_kept_entry, description_of_items_entry
    additems_destroyer()
    additems_frame = tk.Frame(prev_malkhana_frame.master)
    additems_frame.master.title("Add Items")
    additems_frame.pack(fill=tk.BOTH, expand=True)

    # Apply Radiance theme
    style = ThemedStyle(additems_frame)
    style.theme_use('radiance')

    # Labels
    font_style = ('Helvetica', 12)
    tk.Label(additems_frame, text="Barcode Number:", font=font_style).grid(
        row=0, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="FIR Number:", font=font_style).grid(
        row=1, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Seized Items:", font=font_style).grid(
        row=2, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="IPC Section:", font=font_style).grid(
        row=3, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Crime Location:", font=font_style).grid(
        row=4, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Crime Date:", font=font_style).grid(
        row=5, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Crime Time:", font=font_style).grid(
        row=6, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Crime Witnesses:", font=font_style).grid(
        row=7, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Crime Inspector:", font=font_style).grid(
        row=8, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Where Kept:", font=font_style).grid(
        row=9, column=0, padx=10, pady=10, sticky="w")
    tk.Label(additems_frame, text="Description of Item:", font=font_style).grid(
        row=10, column=0, padx=10, pady=10, sticky="w")

    # Entry Fields
    textbox_font = ('Helvetica', 12)
    barcode_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    fir_no_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    seized_items_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    ipc_section_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    crime_location_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    crime_date_entry = DateEntry(additems_frame, font=textbox_font,
                                 width=12, background='darkblue', foreground='white', borderwidth=2)
    hour_var = tk.StringVar(additems_frame, value='00')
    minute_var = tk.StringVar(additems_frame, value='00')

    hour_menu = ttk.Combobox(additems_frame, font=textbox_font, textvariable=hour_var, values=[
                             str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_menu = ttk.Combobox(additems_frame, font=textbox_font, textvariable=minute_var, values=[
                               str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    crime_witness_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    crime_inspector_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    where_kept_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)
    description_of_items_entry = tk.Entry(
        additems_frame, background="#FFFFFF", font=textbox_font)

    # Place Entry Fields
    barcode_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    fir_no_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    seized_items_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    ipc_section_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    crime_location_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    crime_date_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
    crime_witness_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
    crime_inspector_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
    description_of_items_entry.grid(
        row=10, column=1, padx=10, pady=10, sticky="w")
    where_kept_entry.grid(row=9, column=1, padx=10, pady=10, sticky="w")
    hour_menu.grid(row=6, column=1, padx=10, pady=10, sticky="w")
    minute_menu.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    button_font = ('Helvetica', 12)
    add_attachment_button = tk.Button(
        additems_frame, text="Add Attachment", background="#FFFFFF", command=browse_file, font=button_font)

    add_attachment_button.grid(
        row=11, column=1, padx=10, pady=10, sticky="w")

    add_item_button = tk.Button(additems_frame, text="Add Item",
                                background="#FFFFFF", command=insert_data, font=button_font)
    add_item_button.grid(row=13, column=0, columnspan=4,
                         padx=10, pady=10, sticky="ew")

    back_button = tk.Button(additems_frame, text="Back",
                            background="#FFFFFF", command=go_back, font=button_font)
    back_button.grid(row=0, column=30, padx=10, pady=10, sticky="w")

    home_button = tk.Button(additems_frame, text="Home",
                            background="#FFFFFF", command=go_home, font=button_font)
    home_button.grid(row=0, column=31, padx=10, pady=10, sticky="w")

    logout = tk.Button(additems_frame, text="Log Out",
                       background="#FFFFFF", command=logoutclicked, font=button_font)
    logout.grid(row=0, column=32, padx=10, pady=10, sticky="w")

    additems_frame.mainloop()


def insert_data():

    global barcode_entry, fir_no_entry, seized_items_entry, ipc_section_entry, crime_location_entry, crime_date_entry, hour_var, minute_var, crime_witness_entry, crime_inspector_entry, where_kept_entry, description_of_items_entry
    barcode = barcode_entry.get()
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    ipc_section = ipc_section_entry.get()
    crime_location = crime_location_entry.get()
    crime_date = crime_date_entry.get()
    crime_witness = crime_witness_entry.get()
    crime_inspector = crime_inspector_entry.get()
    where_kept = where_kept_entry.get()
    description_of_items = description_of_items_entry.get()

    crime_hour = int(hour_var.get())
    crime_minute = int(minute_var.get())
    crime_time = f"{crime_hour:02d}:{crime_minute:02d}"

    if file_path:
        with open(file_path, 'rb') as file:
            image_data = file.read()
    else:
        messagebox.showinfo("Error , Add Attachment.!")

    try:
        conn = sqlite3.connect('databases/attachments.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS attachments (
                            barcode INTEGER PRIMARY KEY,
                            attachment_data BLOB
                        );''')
        conn.commit()
        conn.close()
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('databases/items_in_malkhana.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            barcode INTEGER PRIMARY KEY ,
                            fir_no TEXT,
                            seized_items TEXT,
                            ipc_section TEXT,
                            crime_location TEXT,
                            crime_date TEXT,
                            crime_time TEXT,
                            crime_witness TEXT,
                            crime_inspector TEXT,
                            item_status TEXT,
                            where_kept TEXT,
                            description_of_items TEXT,
                            entry_time TEXT,
                            attachments BLOB
                        );''')

        entry_time = datetime.datetime.now()
        item_status = "malkhana"

        # Execute the SQL command to insert data into the table
        cursor.execute('''INSERT INTO items (barcode,fir_no, seized_items, ipc_section, 
                          crime_location, crime_date, crime_time, crime_witness, 
                          crime_inspector,item_status,where_kept,description_of_items,entry_time,attachments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (barcode, fir_no, seized_items, ipc_section, crime_location, crime_date,
                        crime_time, crime_witness, crime_inspector, item_status, where_kept, description_of_items, entry_time, image_data))

        if file_path:
            save_attachment(barcode, file_path)

        # Commit the changes
        conn.commit()
        conn.close()
        activity = "\nAdded item barcode no: "+barcode
        lu.log_activity(login.current_user, activity)

        # Clear the entry fields
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        ipc_section_entry.delete(0, tk.END)
        crime_location_entry.delete(0, tk.END)
        crime_date_entry.delete(0, tk.END)
        crime_witness_entry.delete(0, tk.END)
        crime_inspector_entry.delete(0, tk.END)
        where_kept_entry.delete(0, tk.END)
        description_of_items_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Successful", "Item Stored Successfully!" + activity)

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")


def browse_file():
    global file_path, file_entry

    # Ask user to select a file for attachment
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry = file_path


def save_attachment(barcode, file_path):
    with open(file_path, 'rb') as file:
        attachment_data = file.read()

    conn = sqlite3.connect('databases/attachments.db')
    cursor = conn.cursor()

    # Delete any existing entry for the barcode
    cursor.execute("DELETE FROM attachments WHERE barcode = ?", (barcode,))

    # Insert the new attachment
    cursor.execute(
        "INSERT INTO attachments (barcode, attachment_data) VALUES (?, ?)", (barcode, attachment_data))

    conn.commit()
    conn.close()


def go_back():
    additems_destroyer()
    m.mkpage(additems_frame)


def go_home():
    additems_destroyer()
    Homepage.open_homepage(additems_frame)


def logoutclicked():
    activity = "LOG-OUT"
    lu.log_activity(login.current_user, activity)
    additems_destroyer()
    login.initloginpage(additems_frame)


def additems_destroyer():
    if additems_frame is not None:
        additems_frame.destroy()
