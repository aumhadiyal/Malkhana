import tkinter as tk
import MalkhanaTable.additems.additems as a
import home.Homepage as Homepage
import MalkhanaTable.checkin.checkinpage as cp
import Log.log as log
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
import logger as lu
import login.login as login

fsl_checkin_frame = None


def update_item_status(barcode, checkin_date, checkin_time,
                       order_no, examiner, examiner_report):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='malkhana' where barcode = ?", (barcode,))
    con.commit()
    con.close()
    conn = sqlite3.connect("databases/fsl_records.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE fsl_records SET checkin_date = ?,checkin_time=?,examiner_name=?,fsl_report = ? WHERE order_no = ?",
                   (checkin_date, checkin_time, examiner, examiner_report, order_no))
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    order_no_entry.delete(0, tk.END)
    examiner_report_entry.delete("1.0", tk.END)
    conn.commit()
    conn.close()
    messagebox.showinfo("Successful", "Succesfully entered into Malkhana")
    log.update_logs(barcode, "Checkin From FSL",
                    checkin_date, checkin_time)
    activity = "Item checked in from FSL barcode no: "+barcode
    lu.log_activity(login.current_user, activity)


def checkin():
    barcode = barcode_entry.get()
    checkin_time = f"{hour_var.get()}:{minute_var.get()}"
    checkin_date = checkin_date_entry.get_date()
    order_no = order_no_entry.get()
    examiner = examiner_entry.get()
    examiner_report = examiner_report_entry.get("1.0", "end-1c")

    barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)


def checkin_page(prev_checkin_page):
    global fsl_checkin_frame, barcode_entry, order_no_entry, checkin_date_entry, hour_var, minute_var, examiner_report_entry, examiner_entry
    fsL_checkin_destroyer()
    fsl_checkin_frame = tk.Frame(prev_checkin_page.master)
    fsl_checkin_frame.master.title("Checkin From FSL")

    # Use pack for the fsl_checkin_frame
    fsl_checkin_frame.pack(fill=tk.BOTH, expand=True)

    # Labels
    label_barcode_no = ttk.Label(
        fsl_checkin_frame, text="Barcode No:", background="#B9E6FF", font=("Helvetica", 12))
    label_order_no = ttk.Label(
        fsl_checkin_frame, text="Order No:",  background="#B9E6FF", font=("Helvetica", 12))
    label_checkin_time = ttk.Label(
        fsl_checkin_frame, text="Checkin Time:", background="#B9E6FF", font=("Helvetica", 12))
    label_checkin_date = ttk.Label(
        fsl_checkin_frame, text="Checkin Date:", background="#B9E6FF", font=("Helvetica", 12))
    label_examiner = ttk.Label(
        fsl_checkin_frame, text="Examiner Name:",  background="#B9E6FF", font=("Helvetica", 12))
    label_examiner_report = ttk.Label(
        fsl_checkin_frame, text="Examiner Report:",  background="#B9E6FF", font=("Helvetica", 12))

    label_barcode_no.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    label_order_no.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    label_checkin_time.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    label_checkin_date.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    label_examiner.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    label_examiner_report.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

    # Entry fields
    barcode_entry = ttk.Entry(fsl_checkin_frame, font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    barcode_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    order_no_entry = ttk.Entry(fsl_checkin_frame, font=("Helvetica", 12))
    order_no_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    hour_var = tk.StringVar(fsl_checkin_frame, value='00')
    minute_var = tk.StringVar(fsl_checkin_frame, value='00')

    hour_menu = ttk.Combobox(fsl_checkin_frame, textvariable=hour_var, values=[
                             str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_menu = ttk.Combobox(fsl_checkin_frame, textvariable=minute_var, values=[
                               str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    hour_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
    minute_menu.grid(row=2, column=3, columnspan=2,
                     padx=5, pady=5, sticky=tk.W)

    # Date field using tkcalendar
    checkin_date_entry = DateEntry(
        fsl_checkin_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    # Use sticky=tk.W for left alignment
    checkin_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    examiner_entry = ttk.Entry(
        fsl_checkin_frame,  background="#FFFFFF", font=("Helvetica", 12))
    examiner_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    # Text area for examiner report
    examiner_report_entry = tk.Text(
        fsl_checkin_frame, height=5, background="#FFFFFF", width=30, font=("Helvetica", 12))
    # Use sticky=tk.W for left alignment
    examiner_report_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    # Check-in button
    checkin_button = tk.Button(fsl_checkin_frame, text="Checkin",
                               background="#FFFFFF", command=checkin, font=("Helvetica", 12))
    checkin_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    Home = tk.Button(fsl_checkin_frame, text="Homepage",
                     background="#FFFFFF", command=go_home, font=("Helvetica", 12))
    Home.grid(row=7, column=0, padx=10, pady=10, sticky=tk.E)

    back_button = tk.Button(fsl_checkin_frame, text="Back",
                            background="#FFFFFF", command=go_back, font=("Helvetica", 12))
    back_button.grid(row=7, column=1, padx=10, pady=10, sticky=tk.W)


def go_home():
    fsL_checkin_destroyer()
    Homepage.open_homepage_r(fsl_checkin_frame)


def go_back():
    fsL_checkin_destroyer()
    cp.CIpage(fsl_checkin_frame)


def fsL_checkin_destroyer():
    if fsl_checkin_frame is not None:
        fsl_checkin_frame.destroy()


def barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found",
                             "Entered Barcode Not Found In Database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
        return

    already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    examiner_report_entry.delete("1.0", tk.END)


def already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("fsl", "FSL"):
        update_item_status(barcode, checkin_date, checkin_time,
                           order_no, examiner, examiner_report)

    else:
        messagebox.showerror("Item Error",
                             "Item exists in Malkhana/Court .")
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
