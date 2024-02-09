import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import home.Homepage as homepage
import login.login as login
import logger as lu
from PIL import Image,ImageTk

court_frame = None


def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def view_court(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global court_frame
    court_destroyer()
    court_frame = tk.Frame(prev_malkhana_frame.master)
    court_frame.master.title("Court Info")
    court_frame.pack(fill=tk.BOTH, expand=True)

     # Get screen width and height
    screen_width = court_frame.winfo_screenwidth()
    screen_height = court_frame.winfo_screenheight()

    # Load and resize background image
    bg_image = Image.open("bg.jpeg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(court_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tree = ttk.Treeview(court_frame)

    x_scrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)
    y_scrollbar = ttk.Scrollbar(tree, orient=tk.VERTICAL, command=tree.yview)

    tree.configure(xscrollcommand=x_scrollbar.set,
                   yscrollcommand=y_scrollbar.set)

    tree["columns"] = (
        "Barcode",
        "FIR Number",
        "Seized Items",
        "Checkout Date",
        "Checkout Time",
        "Undertaking Officer",
        "Checkin Date",
        "Checkin Time",
        "Order Details"
    )

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Barcode", anchor=tk.W, width=100)
    tree.column("FIR Number", anchor=tk.W, width=100)
    tree.column("Seized Items", anchor=tk.W, width=150)
    tree.column("Checkout Date", anchor=tk.W, width=100)
    tree.column("Checkout Time", anchor=tk.W, width=100)
    tree.column("Undertaking Officer", anchor=tk.W, width=150)
    tree.column("Checkin Date", anchor=tk.W, width=100)
    tree.column("Checkin Time", anchor=tk.W, width=100)
    tree.column("Order Details", anchor=tk.W, width=100)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("Checkout Date", text="Checkout Date", anchor=tk.W)
    tree.heading("Checkout Time", text="Checkout Time", anchor=tk.W)
    tree.heading("Undertaking Officer",
                 text="Undertaking Officer", anchor=tk.W)
    tree.heading("Checkin Date", text="Checkin Date", anchor=tk.W)
    tree.heading("Checkin Time", text="Checkin Time", anchor=tk.W)
    tree.heading("Order Details", text="Order Details", anchor=tk.W)

    try:
        conn = sqlite3.connect('databases/court_records.db')
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT * FROM court_records ORDER by entry_time DESC''')

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.commit()
        conn.close()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

    tree.pack(fill=tk.BOTH, expand=True)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    back_button = tk.Button(court_frame, text="Back",
                            background="#FFFFFF", command=go_back, font=("Helvetica", 12))
    back_button.pack(pady=10)

    logout = tk.Button(court_frame, text="Log Out", background="#FFFFFF",
                       command=logout_clicked, font=("Helvetica", 12))
    logout.pack(padx=12, pady=10)

    search_var = tk.StringVar()
    search_entry = tk.Entry(court_frame, textvariable=search_var)
    search_entry.pack(pady=5)

    search_field_var = tk.StringVar(value="Barcode")
    search_field_menu = ttk.Combobox(
        court_frame, textvariable=search_field_var, values=tree["columns"], state='readonly')
    search_field_menu.pack()

    search_button = tk.Button(court_frame, text="Search", background="#FFFFFF", command=lambda: search_court(
        tree, search_field_var.get(), search_var.get()), font=("Helvetica", 12))
    search_button.pack()

    show_all_btn = tk.Button(court_frame, text="Show All",  background="#FFFFFF",
                             command=lambda: show_all_court(tree), font=("Helvetica", 12))
    show_all_btn.pack()


def search_court(tree, search_field, search_text):
    for item in tree.get_children():
        tree.delete(item)

    column_mapping = {
        "Barcode": "barcode",
        "FIR Number": "fir_no",
        "Seized Items": "seized_items",
        "Checkout Date": "checkout_date",
        "Checkout Time": "checkout_time",
        "Undertaking Officer": "taken_by_whom",
        "Checkin Date": "checkin_date",
        "Checkin Time": "checkin_time",
        "Order Details": "order_details"
    }

    actual_column_name = column_mapping.get(search_field)

    if actual_column_name is None:
        tk.messagebox.showerror(
            "Error", f"Invalid search field: {search_field}")
        return

    try:
        conn = sqlite3.connect('databases/court_records.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM court_records
            WHERE {actual_column_name} LIKE ?
        ''', ('%' + search_text + '%',))

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.commit()
        conn.close()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")


def show_all_court(tree):
    for item in tree.get_children():
        tree.delete(item)
    try:
        conn = sqlite3.connect("databases/court_records.db")
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM court_records ORDER BY entry_time DESC''')
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.commit()
        conn.close()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")


def court_destroyer():
    if court_frame is not None:
        court_frame.destroy()


def go_back():
    court_destroyer()
    homepage.open_homepage(court_frame)


def go_home():
    court_destroyer()
    homepage.open_homepage(court_frame)


def logout_clicked():
    activity = "LOG-OUT"
    lu.log_activity(login.current_user, activity)
    court_destroyer()
    login.init_login_page(court_frame)
