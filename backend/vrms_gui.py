# =============================================================================
# AI DISCLOSURE
# Tool used: Claude
# AI-generated parts: UI layout, Insert Vehicle form validation and display table.
# =============================================================================

# REQUIREMENTS:
#   pip install customtkinter mysql-connector-python

import customtkinter as ctk
import mysql.connector
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import urllib.request
from dotenv import load_dotenv
import os

load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

#COLORS
NAVY        = "#081E3F"
NAVY_HOVER  = "#0a2a57"
SKY         = "#38BDF8"
SKY_HOVER   = "#7DD3FC"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Vehicle Rental Management System")
app.geometry("860x640")
app.resizable(False, False)
app.configure(fg_color="#F4F6F9")

header = ctk.CTkFrame(app, fg_color=NAVY, corner_radius=0, height=70)
header.pack(fill="x")
header.pack_propagate(False)

try:
    img = Image.open("icon.png").convert("RGBA").resize((46, 46), Image.LANCZOS)
    icon_img = ctk.CTkImage(light_image=img, dark_image=img, size=(46, 46))
    icon_label = ctk.CTkLabel(header, image=icon_img, text="", fg_color="transparent")
    icon_label.pack(side="left", padx=(18, 10), pady=12)
except Exception:
    # fallback: just show a placeholder text if icon.png is missing
    ctk.CTkLabel(header, text="🚗", font=ctk.CTkFont(size=28),
                 fg_color="transparent", text_color="white")\
        .pack(side="left", padx=(18, 10), pady=12)

title_frame = ctk.CTkFrame(header, fg_color="transparent")
title_frame.pack(side="left", pady=12)
ctk.CTkLabel(title_frame, text="Vehicle Rental Management System",
             font=ctk.CTkFont(size=15, weight="bold"),
             text_color="#FFFFFF").pack(anchor="w")
ctk.CTkLabel(title_frame, text="VRMS — Part 2 Interface",
             font=ctk.CTkFont(size=11),
             text_color="#90afd4").pack(anchor="w")

# DB status pill
status_frame = ctk.CTkFrame(header, fg_color="#ffffff",
                              corner_radius=20, border_width=1,
                              border_color="#ffffff")
status_frame.pack(side="right", padx=18, pady=18)
status_dot = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=10),
                           text_color="#90afd4", width=14)
status_dot.pack(side="left", padx=(10, 2))
status_label = ctk.CTkLabel(status_frame, text="Connecting...",
                             font=ctk.CTkFont(size=12, weight="bold"),
                             text_color="#FFFFFF")
status_label.pack(side="left", padx=(0, 12), pady=6)

def check_connection():
    try:
        conn = get_connection()
        conn.close()
        status_dot.configure(text_color="#4caf50")
        status_label.configure(text="MySQL connected")
    except Exception:
        status_dot.configure(text_color="#e24b4a")
        status_label.configure(text="Not connected")

app.after(500, check_connection)

tabs = ctk.CTkTabview(app, fg_color="#F4F6F9",
                      segmented_button_fg_color="#F4F6F9",
                      segmented_button_selected_color=NAVY,
                      segmented_button_selected_hover_color=NAVY_HOVER,
                      segmented_button_unselected_color="#F4F6F9",
                      segmented_button_unselected_hover_color="#e2e8f0",
                      text_color="#64748b",
                      text_color_disabled="#64748b")
tabs.pack(fill="both", expand=True, padx=16, pady=(10, 16))
tabs.add("  Insert Vehicle  ")
tabs.add("  Rental Agreements  ")

def section_label(parent, text, row, col=0, span=2):
    ctk.CTkLabel(parent, text=text.upper(),
                 font=ctk.CTkFont(size=10, weight="bold"),
                 text_color="#94a3b8").grid(
        row=row, column=col, columnspan=span,
        padx=16, pady=(14, 4), sticky="w")

def make_field(parent, label, row, col, placeholder="", required=True):
    star = " *" if required else ""
    ctk.CTkLabel(parent, text=label + star,
                 font=ctk.CTkFont(size=12),
                 text_color="#475569").grid(
        row=row, column=col, padx=(16, 4), pady=(0, 2), sticky="sw")
    e = ctk.CTkEntry(parent, width=240, placeholder_text=placeholder,
                     fg_color="white", border_color="#cbd5e1",
                     text_color="#1e293b")
    e.grid(row=row+1, column=col, padx=(16, 4), pady=(0, 8), sticky="w")
    return e

t1 = tabs.tab("  Insert Vehicle  ")
t1.grid_columnconfigure((0, 1), weight=1)

fields = {}
section_label(t1, "Vehicle Information", 0)
fields["VehicleID"]    = make_field(t1, "Vehicle ID",    1, 0, "e.g. 101")
fields["LicensePlate"] = make_field(t1, "License Plate", 1, 1, "e.g. ABC-1234")
fields["Make"]         = make_field(t1, "Make",          3, 0, "e.g. Toyota")
fields["Model"]        = make_field(t1, "Model",         3, 1, "e.g. Corolla")
fields["Year"]         = make_field(t1, "Year",          5, 0, "e.g. 2022")
fields["Color"]        = make_field(t1, "Color",         5, 1, "e.g. Red", required=False)

section_label(t1, "Rates & Assignment", 7)
fields["DailyRentalRate"] = make_field(t1, "Daily Rate ($)",   8,  0, "e.g. 49.99")
fields["CurrentMileage"]  = make_field(t1, "Current Mileage",  8,  1, "e.g. 15000")
fields["TypeID"]           = make_field(t1, "Type ID",         10, 0, "e.g. 1")
fields["BranchID"]         = make_field(t1, "Branch ID",       10, 1, "e.g. 1")

insert_feedback = ctk.CTkLabel(t1, text="",
                                font=ctk.CTkFont(size=12),
                                text_color="#16a34a")
insert_feedback.grid(row=13, column=0, columnspan=2, pady=(4, 0), sticky="w", padx=16)

def validate_and_insert():
    data = {k: v.get().strip() for k, v in fields.items()}

    required = ["VehicleID","LicensePlate","Make","Model","Year",
                "DailyRentalRate","CurrentMileage","TypeID","BranchID"]
    for r in required:
        if not data[r]:
            messagebox.showerror("Validation Error", f"{r} is required.")
            return
    try:
        vid  = int(data["VehicleID"])
        year = int(data["Year"])
        mil  = int(data["CurrentMileage"])
        rate = float(data["DailyRentalRate"])
        tid  = int(data["TypeID"])
        bid  = int(data["BranchID"])
    except ValueError:
        messagebox.showerror("Validation Error",
            "VehicleID, Year, Mileage, TypeID, BranchID must be integers.\n"
            "Daily Rate must be a number.")
        return
    if year < 1900 or year > 2100:
        messagebox.showerror("Validation Error", "Enter a valid year.")
        return
    if rate <= 0:
        messagebox.showerror("Validation Error", "Daily Rate must be > 0.")
        return
    if mil < 0:
        messagebox.showerror("Validation Error", "Mileage cannot be negative.")
        return

    sql = """INSERT INTO Vehicle
             (VehicleID,LicensePlate,Make,Model,`Year`,Color,
              DailyRentalRate,CurrentMileage,TypeID,BranchID)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    vals = (vid, data["LicensePlate"], data["Make"], data["Model"],
            year, data["Color"] or None, rate, mil, tid, bid)
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(sql, vals)
        conn.commit()
        conn.close()
        insert_feedback.configure(text="✔  Vehicle inserted successfully!", text_color="#16a34a")
        for e in fields.values():
            e.delete(0, "end")
        app.after(4000, lambda: insert_feedback.configure(text=""))
    except mysql.connector.IntegrityError as e:
        messagebox.showerror("DB Error", f"Integrity error:\n{e}")
    except mysql.connector.Error as e:
        messagebox.showerror("DB Error", f"Database error:\n{e}")

ctk.CTkButton(t1, text="Insert Vehicle",
              fg_color=SKY, hover_color=SKY_HOVER,
              text_color=NAVY, font=ctk.CTkFont(size=13, weight="bold"),
              width=200, height=38,
              command=validate_and_insert).grid(
    row=12, column=0, columnspan=2, pady=(12, 4), padx=16, sticky="w")

t2 = tabs.tab("  Rental Agreements  ")
search_row = ctk.CTkFrame(t2, fg_color="transparent")
search_row.pack(fill="x", padx=4, pady=(4, 12))

ctk.CTkLabel(search_row, text="Customer ID",
             font=ctk.CTkFont(size=12), text_color="#475569").pack(side="left", padx=(0, 8))
cid_entry = ctk.CTkEntry(search_row, width=150, placeholder_text="e.g. 5",
                          fg_color="white", border_color="#cbd5e1", text_color="#1e293b")
cid_entry.pack(side="left", padx=(0, 10))
ctk.CTkButton(search_row, text="Search",
              fg_color=NAVY, hover_color=NAVY_HOVER,
              text_color="white", font=ctk.CTkFont(size=13, weight="bold"),
              width=100, height=34,
              command=lambda: search_agreements()).pack(side="left")
result_count = ctk.CTkLabel(search_row, text="",
                             font=ctk.CTkFont(size=12), text_color="#64748b")
result_count.pack(side="left", padx=12)

# Treeview table
tree_wrap = ctk.CTkFrame(t2, fg_color="white",
                          corner_radius=8, border_width=1, border_color="#e2e8f0")
tree_wrap.pack(fill="both", expand=True, padx=4)

cols = ("AgreementID","VehicleID","Pickup Branch","Return Branch",
        "Sched. Pickup","Sched. Return","Status","Est. Cost","Act. Cost")

style = ttk.Style()
style.theme_use("clam")
style.configure("VRMS.Treeview",
    background="white", fieldbackground="white",
    foreground="#1e293b", rowheight=30, font=("Arial", 11))
style.configure("VRMS.Treeview.Heading",
    background=NAVY, foreground="white",
    font=("Arial", 10, "bold"), relief="flat")
style.map("VRMS.Treeview",
    background=[("selected", "#dbeafe")],
    foreground=[("selected", NAVY)])

tree = ttk.Treeview(tree_wrap, columns=cols, show="headings",
                    height=12, style="VRMS.Treeview")

col_widths = [95, 75, 105, 105, 135, 135, 75, 80, 80]
for c, w in zip(cols, col_widths):
    tree.heading(c, text=c)
    tree.column(c, width=w, anchor="center", stretch=False)

vsb = ttk.Scrollbar(tree_wrap, orient="vertical",   command=tree.yview)
hsb = ttk.Scrollbar(tree_wrap, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")
tree_wrap.grid_rowconfigure(0, weight=1)
tree_wrap.grid_columnconfigure(0, weight=1)

def search_agreements():
    cid = cid_entry.get().strip()
    if not cid:
        messagebox.showerror("Input Error", "Please enter a Customer ID.")
        return
    try:
        cid = int(cid)
    except ValueError:
        messagebox.showerror("Input Error", "Customer ID must be an integer.")
        return

    sql = """SELECT AgreementID, VehicleID, PickupBranchID, ReturnBranchID,
                    ScheduledPickupDateTime, ScheduledReturnDateTime,
                    Status, EstimatedCost, ActualCost
             FROM   RentalAgreement
             WHERE  CustomerID = %s
             ORDER BY ScheduledPickupDateTime DESC"""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(sql, (cid,))
        rows = cur.fetchall()
        conn.close()
        for row in tree.get_children():
            tree.delete(row)
        if not rows:
            result_count.configure(text="No agreements found.", text_color="#f59e0b")
        else:
            result_count.configure(
                text=f"{len(rows)} agreement(s) found.", text_color="#16a34a")
            for r in rows:
                tree.insert("", "end", values=[(str(v) if v is not None else "—") for v in r])
    except mysql.connector.Error as e:
        messagebox.showerror("DB Error", f"Database error:\n{e}")

app.mainloop()
