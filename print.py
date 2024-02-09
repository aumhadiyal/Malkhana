import datetime
import io
import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter.tix import IMAGETEXT
import home.Homepage as Homepage
import pandas as pd
import os
from PIL import Image
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage

print_frame = None


def set_custom_theme(root):
    # Load and display background image
    bg_image = Image.open("bg.jpeg")
    # Resize the image to match the window size
    bg_image = bg_image.resize((root.winfo_screenwidth(), 1000), Image.LANCZOS)

    bg_photo = IMAGETEXT.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def print_details(barcode=None):
    try:
        currenttime = str(datetime.datetime.now()).replace(":", "")
        filename = f"{barcode}_{currenttime}.xlsx"

        # Initialize Excel writer with 'w' mode to create the file if not exists
        with pd.ExcelWriter(filename, mode='w') as writer:
            # Fetch data from items_in_malkhana.db and write to Items sheet
            conn_items = sqlite3.connect('databases/items_in_malkhana.db')
            if barcode is None:
                query_items = "SELECT * FROM items"
            else:
                query_items = "SELECT barcode,fir_no,seized_items,ipc_section,crime_location,crime_date,crime_time,crime_witness,crime_inspector,item_status,where_kept,entry_time FROM items WHERE barcode = ?"

            df_items = pd.read_sql_query(
                query_items, conn_items, params=(barcode,))
            conn_items.close()

            df_items.to_excel(writer, sheet_name='Items', index=False)

            # Fetch data from fsl_records.db and write to FSL Records sheet
            conn_fsl = sqlite3.connect('databases/fsl_records.db')
            if barcode is None:
                query_fsl = "SELECT * FROM fsl_records"
            else:
                query_fsl = "SELECT * FROM fsl_records WHERE barcode = ?"

            df_fsl = pd.read_sql_query(query_fsl, conn_fsl, params=(barcode,))
            conn_fsl.close()

            df_fsl.to_excel(writer, sheet_name='FSL Records', index=False)

            # Fetch data from logs.db and write to Logs sheet
            conn_logs = sqlite3.connect('databases/logs.db')
            if barcode is None:
                query_logs = "SELECT * FROM logs"
            else:
                query_logs = "SELECT * FROM logs WHERE barcode = ?"

            df_logs = pd.read_sql_query(
                query_logs, conn_logs, params=(barcode,))
            conn_logs.close()

            df_logs.to_excel(writer, sheet_name='Logs', index=False)

            # Fetch image data from attachments.db and write to Attachments sheet
            conn_attachments = sqlite3.connect('databases/attachments.db')
            query_attachments = "SELECT attachment_data FROM attachments WHERE barcode = ?"

            df_attachments = pd.read_sql_query(
                query_attachments, conn_attachments, params=(barcode,))
            conn_attachments.close()

            if not df_attachments.empty:
                # Encode image data as Base64
                df_attachments['Encoded_Image'] = df_attachments['attachment_data'].apply(
                    lambda x: base64.b64encode(x).decode('utf-8'))

                # Write image data to Attachments sheet
                df_attachments.to_excel(
                    writer, sheet_name='Attachments', index=False)

        messagebox.showinfo(
            "Success", "Data exported to Excel successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def go_home():
    CL_destroyer()
    Homepage.open_homepage(print_frame)


def CL_destroyer():
    if print_frame is not None:
        print_frame.destroy()
