import tkinter as tk
import sqlite3
from tkinter import messagebox
import main
from tkinter import ttk
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as m
import login.login as login
import logger as lu
from PIL import Image,ImageTk
viewfsl_frame = None



def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def viewfsl(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global viewfsl_frame
    fsl_destroyer()
    viewfsl_frame = tk.Frame(prev_malkhana_frame.master)
    viewfsl_frame.master.title("FSL Info")
    viewfsl_frame.pack(fill=tk.BOTH, expand=True)  # To occupy the whole screen

         # Get screen width and height
    screen_width = viewfsl_frame.winfo_screenwidth()
    screen_height = viewfsl_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(viewfsl_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a Treeview widget to display the data in a tabular format
    tree = ttk.Treeview(viewfsl_frame)

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
        "FSL Order Number",
        "Checkout Date",
        "Checkout Time",
        "Undertaking Officer",
        "Checkin Date",
        "Checkin Time",
        "Examiner",
        "FSL Report")

    # Format columns (adjust the widths as per your requirements)
    tree.column("#0", width=0, stretch=tk.NO)  # Hidden first column
    tree.column("Barcode", anchor=tk.W, width=100)
    tree.column("FIR Number", anchor=tk.W, width=100)
    tree.column("Seized Items", anchor=tk.W, width=150)
    tree.column("FSL Order Number", anchor=tk.W, width=100)
    tree.column("Checkout Date", anchor=tk.W, width=100)
    tree.column("Checkout Time", anchor=tk.W, width=100)
    tree.column("Undertaking Officer", anchor=tk.W, width=150)
    tree.column("Checkin Date", anchor=tk.W, width=100)
    tree.column("Checkin Time", anchor=tk.W, width=100)
    tree.column("Examiner", anchor=tk.W, width=150)
    tree.column("FSL Report", anchor=tk.W, width=100)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("FSL Order Number", text="FSL Order Number", anchor=tk.W)
    tree.heading("Checkout Date", text="Checkout Date", anchor=tk.W)
    tree.heading("Checkout Time", text="Checkout Time", anchor=tk.W)
    tree.heading("Undertaking Officer",
                 text="Undertaking Officer", anchor=tk.W)
    tree.heading("Checkin Date", text="Checkin Date", anchor=tk.W)
    tree.heading("Checkin Time", text="Checkin Time", anchor=tk.W)
    tree.heading("Examiner", text="Examiner", anchor=tk.W)
    tree.heading("FSL Report", text="FSL Report", anchor=tk.W)

    # Add data to the treeview from the database
    try:
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('databases/fsl_records.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        # Execute the SQL command to select all rows from the table
        cursor.execute(
            '''SELECT * FROM fsl_records ORDER by entry_time DESC''')

        # Fetch all the rows and insert them into the treeview
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()

    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

    # Pack the treeview widget with a scrollbar
    tree.pack(fill=tk.BOTH, expand=True)

    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a button to go back to the homepage
    back_button = tk.Button(viewfsl_frame, text="Back",
                            background="#FFFFFF", command=go_back, font=("Helvetica", 12))
    back_button.pack(pady=10)

    logout = tk.Button(viewfsl_frame, text="Log Out", background="#FFFFFF",
                       command=logoutclicked, font=("Helvetica", 12))
    logout.pack(padx=12, pady=10)

    # Create a search entry and button
    search_var = tk.StringVar()
    search_entry = tk.Entry(viewfsl_frame, textvariable=search_var)
    search_entry.pack(pady=5)

    # Create a dropdown menu for selecting search field
    search_field_var = tk.StringVar(value="Barcode")
    search_field_menu = ttk.Combobox(
        viewfsl_frame, textvariable=search_field_var, values=tree["columns"], state='readonly')
    search_field_menu.pack()

    search_button = tk.Button(viewfsl_frame, text="Search", background="#FFFFFF", command=lambda: search_fsl(
        tree, search_field_var.get(), search_var.get()), font=("Helvetica", 12))
    search_button.pack()

    show_all_btn = tk.Button(viewfsl_frame, text="Show All",  background="#FFFFFF",
                             command=lambda: show_all_fsl(tree), font=("Helvetica", 12))
    show_all_btn.pack()


def search_fsl(tree, search_field, search_text):
    # Clear previous search results
    for item in tree.get_children():
        tree.delete(item)

    # Map the user-visible column name to the actual column name in the database
    column_mapping = {
        "Barcode": "barcode",
        "FIR Number": "fir_number",
        "Seized Items": "seized_items",
        "FSL Order Number": "order_no",
        "Checkout Date": "checkout_date",
        "Checkout Time": "checkout_time",
        "Undertaking Officer": "taken_by_whom",
        "Checkin Date": "checkin_date",
        "Checkin Time": "checkin_time",
        "Examiner": "examiner_name",
        "FSL Report": "fsl_report"
    }

    # Get the actual column name from the mapping
    actual_column_name = column_mapping.get(search_field)

    if actual_column_name is None:
        # Display an error message if the user-visible column name is not found in the mapping
        tk.messagebox.showerror(
            "Error", f"Invalid search field: {search_field}")
        return

    # Add data to the treeview from the database based on the search criteria
    try:
        conn = sqlite3.connect('databases/fsl_records.db')
        cursor = conn.cursor()

        # Construct the SQL query dynamically using the actual column name
        cursor.execute(f'''
            SELECT * FROM fsl_records
            WHERE {actual_column_name} LIKE ?
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


def show_all_fsl(tree):
    for item in tree.get_children():
        tree.delete(item)
    try:
        conn = sqlite3.connect("databases/fsl_records.db")
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM fsl_records ORDER BY entry_time DESC''')
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
        "FSL ઓર્ડર નંબર": "fsl_order_no",
        "ચેકઆઉટ તારીખ": "checkout_date",
        "ચેકઆઉટ સમય": "checkout_time",
        "કોણ લેવી છે": "taken_by_whom",
        "ચેક ઇન તારીખ": "checkin_date",
        "ચેક ઇન સમય": "checkin_time",
        "તપાસક નું નામ": "examiner_name",
        "FSL રિપોર્ટ": "fsl_report"
    }

    return gujarati_to_english.get(column_name_gujarati, column_name_gujarati)


def fsl_destroyer():
    if viewfsl_frame is not None:
        viewfsl_frame.destroy()


def go_back():
    fsl_destroyer()
    homepage.open_homepage(viewfsl_frame)


def go_home():
    fsl_destroyer()
    homepage.open_homepage(viewfsl_frame)


def logoutclicked():
    activity = "LOG-OUT"
    lu.log_activity(login.current_user, activity)
    fsl_destroyer()
    login.initloginpage(viewfsl_frame)
  # For testing the viewfsl function
