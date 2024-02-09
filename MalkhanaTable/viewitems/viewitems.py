import tkinter as tk
import sqlite3
from tkinter import messagebox
import main
from tkinter import ttk
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as m
import login.login as login
from PIL import Image, ImageTk
import os
import MalkhanaTable.additems.additems as ai
import io
import logger as lu
from PIL import Image, ImageTk
import print


viewitems_frame = None


def viewitems(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global viewitems_frame, tree
    viewitems_frame = tk.Frame(prev_malkhana_frame.master)
    viewitems_frame.master.title("View Items")

    # To occupy the whole screen
    viewitems_frame.pack(fill=tk.BOTH, expand=True)

    # Create a Treeview widget to display the data in a tabular format
    tree = ttk.Treeview(viewitems_frame)
    x_scrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)
    y_scrollbar = ttk.Scrollbar(tree, orient=tk.VERTICAL, command=tree.yview)

    # Configure the treeview to use the scrollbars
    tree.configure(xscrollcommand=x_scrollbar.set,
                   yscrollcommand=y_scrollbar.set)

    # Define columns
    tree["columns"] = (
        "Barcode",
        "FIR Number",
        "Seized Items",
        "IPC Section",
        "Crime Location",
        "Crime Date",
        "Crime Time",
        "Crime Witness",
        "Crime Inspector",
        "Item Status",
        "Where Kept",
        "Item Description"
        # "attachments"
    )

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hidden first column
    tree.column("Barcode", anchor=tk.W, width=80)
    tree.column("FIR Number", anchor=tk.W, width=100)
    tree.column("Seized Items", anchor=tk.W, width=150)
    tree.column("IPC Section", anchor=tk.W, width=100)
    tree.column("Crime Location", anchor=tk.W, width=150)
    tree.column("Crime Date", anchor=tk.W, width=60)
    tree.column("Crime Time", anchor=tk.W, width=60)
    tree.column("Crime Witness", anchor=tk.W, width=150)
    tree.column("Crime Inspector", anchor=tk.W, width=150)
    tree.column("Item Status", anchor=tk.W, width=100)
    tree.column("Where Kept", anchor=tk.W, width=150)
    tree.column("Item Description", anchor=tk.W, width=200)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("IPC Section", text="IPC Section", anchor=tk.W)
    tree.heading("Crime Location", text="Crime Location", anchor=tk.W)
    tree.heading("Crime Date", text="Crime Date", anchor=tk.W)
    tree.heading("Crime Time", text="Crime Time", anchor=tk.W)
    tree.heading("Crime Witness", text="Crime Witness", anchor=tk.W)
    tree.heading("Crime Inspector", text="Crime Inspector", anchor=tk.W)
    tree.heading("Item Status", text="Item Status", anchor=tk.W)
    tree.heading("Where Kept", text="Where Kept", anchor=tk.W)
    tree.heading("Item Description", text="Item Description", anchor=tk.W)

    # Add data to the treeview from the database
    try:
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('databases/items_in_malkhana.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        # Execute the SQL command to select all rows from the table
        cursor.execute('''SELECT barcode, fir_no, seized_items, ipc_section, crime_location, crime_date, crime_time, crime_witness, crime_inspector, item_status, where_kept,description_of_items
 FROM items ORDER BY entry_time DESC''')

        # Fetch all the rows and insert them into the treeview
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()

    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

    tree.pack(fill=tk.BOTH, expand=True)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Function to apply the selected filters
    def apply_filters():
        selected_columns = []
        for column, var in checkbox_vars.items():
            if var.get() == 1:
                selected_columns.append(column)
        # Reconfigure treeview columns
        tree["displaycolumns"] = selected_columns

    # Function to create filter window
    def create_filter_window():
        filter_window = tk.Toplevel(viewitems_frame)
        filter_window.title("Select Filters")

        global checkbox_vars
        checkbox_vars = {}

        for idx, column in enumerate(tree["columns"]):
            var = tk.IntVar(value=1)
            checkbox_vars[column] = var
            cb = tk.Checkbutton(filter_window, text=column, variable=var)
            cb.grid(row=idx, column=0, sticky="w")

        apply_button = tk.Button(
            filter_window, text="Apply Filters", command=apply_filters)
        apply_button.grid(row=len(tree["columns"]), column=0, pady=5)

    # Search and filter row
    search_frame = tk.Frame(viewitems_frame)
    search_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    search_label = tk.Label(search_frame, text="Search Field:")
    search_label.pack(side=tk.LEFT)

    search_field_var = tk.StringVar(value="Barcode")
    search_field_menu = ttk.Combobox(
        search_frame, textvariable=search_field_var, values=tree["columns"], state='readonly')
    search_field_menu.pack(side=tk.LEFT, padx=5, pady=5)

    search_entry = tk.Entry(
        search_frame, background="#D3D3D3", textvariable=tk.StringVar())
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)

    select_filter_button = tk.Button(
        search_frame, text="Select Filter", command=create_filter_window)
    select_filter_button.pack(side=tk.LEFT, padx=5, pady=5)

    search_button = tk.Button(search_frame, text="Search", background="#FFFFFF", command=lambda: search_items(
        tree, search_field_var.get(), search_entry.get()), font=("Helvetica", 12))
    search_button.pack(side=tk.LEFT, padx=5, pady=5)

    show_all_btn = tk.Button(search_frame, text="Show All", background="#FFFFFF",
                             command=lambda: show_all(tree), font=("Helvetica", 12))
    show_all_btn.pack(side=tk.LEFT, padx=5, pady=5)

    # Attachments Button
    view_attachment_button = tk.Button(search_frame, background="#FFFFFF",
                                       text="View Attachment", command=view_attachment, font=("Helvetica", 12))
    view_attachment_button.pack(side=tk.RIGHT, padx=5)

    print_details_button = tk.Button(search_frame, background="#FFFFFF",
                                     text="Print Item Details", command=print_item, font=("Helvetica", 12))
    print_details_button.pack(side=tk.RIGHT, padx=5)
# Function definitions for view_attachment, logoutclicked, search_items, show_all, and go_back go here


def view_attachment():
    selected_item = tree.focus()
    # Assuming the barcode is the first value in the row
    barcode = tree.item(selected_item, 'values')[0]

    conn = sqlite3.connect('databases/attachments.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attachment_data FROM attachments WHERE barcode = ?", (barcode,))
    attachment_data = cursor.fetchone()

    conn.close()

    if attachment_data:
        # Access the attachment data from the tuple with index 0
        image_data = attachment_data[0]

        image = Image.open(io.BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

        # Create a new window to display the image
        image_window = tk.Toplevel(viewitems_frame)
        image_window.title("View Attachment")
        image_label = tk.Label(image_window, image=photo)
        image_label.photo = photo  # Keep a reference to the PhotoImage object
        image_label.pack()
    else:
        messagebox.showinfo("Attachment Not Available!")


def print_item():
    selected_item = tree.focus()
    # Assuming the barcode is the first value in the row
    barcode = tree.item(selected_item, 'values')[0]

    print.print_details(barcode)


def go_back():
    viewitems_destroyer()
    m.mkpage(viewitems_frame)


def viewitems_destroyer():
    if viewitems_frame is not None:
        viewitems_frame.destroy()


def go_home():
    viewitems_destroyer()
    homepage.open_homepage(viewitems_frame)


# def logoutclicked():
#     activity = "LOG-OUT"
#     lu.log_activity(login.current_user, activity)
#     viewitems_destroyer()
#     login.initloginpage(viewitems_frame)


def show_all(tree):
    for item in tree.get_children():
        tree.delete(item)
    try:
        conn = sqlite3.connect("databases/items_in_malkhana.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM items ORDER BY entry_time DESC''')
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()
    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")


def search_items(tree, search_field, search_text):
    # Clear previous search results
    for item in tree.get_children():
        tree.delete(item)

    # Convert the search_field back to the original column name (in English)

    # search_field = convert_to_english(search_field)

    # Add data to the treeview from the database based on the search criteria
    try:
        conn = sqlite3.connect('databases/items_in_malkhana.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM items
            WHERE {search_field} LIKE ?
        ''', ('%' + search_text + '%',))

        # Fetch the rows and insert them into the treeview
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()
    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

# Helper function to convert Gujarati column names to English


def convert_to_english(column_name_gujarati):
    # Replace this with the appropriate mapping from Gujarati to English column names
    gujarati_to_english = {
        "બારકોડ": "barcode",
        "FIR નંબર": "fir_number",
        "વસ્તુનું નામ": "item_name",
        "IPC કલમ": "ipc_section",
        "અપરાધ સ્થળ": "crime_scene",
        "અપરાધ તારીખ": "crime_date",
        "અપરાધ સમય": "crime_time",
        "અપરાધ સાક્ષીઓ": "crime_witnesses",
        "અપરાધ નિરીક્ષક": "crime_inspector",
        "વસ્તુનું અવસ્થા": "item_status",
        "ક્યાં રાખી છે": "where_its_kept"
    }

    return gujarati_to_english.get(column_name_gujarati, column_name_gujarati)
