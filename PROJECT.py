import sqlite3
from tkinter import messagebox, ttk
from tkinter import *

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def add_donor(conn, name, blood_group, contact, entry_name, blood_group_combobox, entry_contact, tree):
    if name and blood_group and contact.isdigit() and len(contact) == 10:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO donors (name, blood_group, contact) VALUES (?, ?, ?)",
                           (name, blood_group, contact))
            conn.commit()

            messagebox.showinfo("Success", "Donor information added successfully!", icon="info")
            clear_entries(entry_name, blood_group_combobox, entry_contact)
            display_donors(conn, tree)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Incomplete or Invalid Information", "Please fill in all the details correctly.", icon="warning")

def display_donors(conn, tree):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donors")
        donors = cursor.fetchall()

        # Clear existing items in the tree
        tree.delete(*tree.get_children())

        for row in donors:
            tree.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def clear_entries(entry_name, blood_group_combobox, entry_contact):
    entry_name.delete(0, END)
    blood_group_combobox.set('')
    entry_contact.delete(0, END)

def add_receiver(conn, name, blood_group, contact, entry_receiver_name, blood_group_receiver_combobox, entry_receiver_contact, tree):
    if name and blood_group and contact.isdigit() and len(contact) == 10:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO receivers (name, blood_group, contact) VALUES (?, ?, ?)",
                           (name, blood_group, contact))
            conn.commit()

            messagebox.showinfo("Success", "Receiver information added successfully!", icon="info")
            clear_entries(entry_receiver_name, blood_group_receiver_combobox, entry_receiver_contact)
            display_receivers(conn, tree)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Incomplete or Invalid Information", "Please fill in all the details correctly.", icon="warning")

def display_receivers(conn, tree):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receivers")
        receivers = cursor.fetchall()

        # Clear existing items in the tree
        tree.delete(*tree.get_children())

        for row in receivers:
            tree.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def clear_receiver_entries(entry_receiver_name, blood_group_receiver_combobox, entry_receiver_contact):
    entry_receiver_name.delete(0, END)
    blood_group_receiver_combobox.set('')
    entry_receiver_contact.delete(0, END)

def close_application(conn, root):
    conn.close()
    root.destroy()

def main():
    root = Tk()
    root.title("Blood Bank Management System")
    root.geometry("1000x600")  # Adjusted window width

    conn = sqlite3.connect("blood_bank.db")
    create_table(conn)

    # Frame for Donors
    donor_frame = Frame(root, bg="#e0f7fa")
    donor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Labels and Entry Widgets for Donors
    label_name = Label(donor_frame, text="Donor Name:", bg="#e0f7fa", font=("Helvetica", 14))
    label_name.grid(row=0, column=0, padx=10, pady=10)
    entry_name = Entry(donor_frame, bg="#b2ebf2", font=("Helvetica", 14))
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_blood_group = Label(donor_frame, text="Blood Group:", bg="#e0f7fa", font=("Helvetica", 14))
    label_blood_group.grid(row=1, column=0, padx=10, pady=10)
    blood_group_var = StringVar()
    blood_group_combobox = ttk.Combobox(donor_frame, textvariable=blood_group_var,
                                        values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                        state="readonly", font=("Helvetica", 14))
    blood_group_combobox.grid(row=1, column=1, padx=10, pady=10)

    label_contact = Label(donor_frame, text="Contact Number:", bg="#e0f7fa", font=("Helvetica", 14))
    label_contact.grid(row=2, column=0, padx=10, pady=10)
    entry_contact = Entry(donor_frame, bg="#b2ebf2", font=("Helvetica", 14))
    entry_contact.grid(row=2, column=1, padx=10, pady=10)

    # Create Treeview for Donors
    columns_donors = ("ID", "Name", "Blood Group", "Contact")
    donor_tree = ttk.Treeview(donor_frame, columns=columns_donors, show="headings", height=13)

    # Set column headings
    for col in columns_donors:
        donor_tree.heading(col, text=col)

    # Add a vertical scrollbar
    scrollbar_donors = ttk.Scrollbar(donor_frame, orient="vertical", command=donor_tree.yview)
    donor_tree.configure(yscrollcommand=scrollbar_donors.set)

    # Add a horizontal scrollbar
    scrollbar_horizontal_donors = ttk.Scrollbar(donor_frame, orient="horizontal", command=donor_tree.xview)
    donor_tree.configure(xscrollcommand=scrollbar_horizontal_donors.set)

    # Grid placement of Treeview and Scrollbars
    donor_tree.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
    scrollbar_donors.grid(row=3, column=2, pady=10, sticky="ns")
    scrollbar_horizontal_donors.grid(row=4, column=0, columnspan=2, sticky="ew")

    # Buttons for Donors
    submit_button = Button(donor_frame, text="Submit Donor", command=lambda: add_donor(conn, entry_name.get(),
                                                                        blood_group_var.get(), entry_contact.get(),
                                                                        entry_name, blood_group_combobox, entry_contact, donor_tree),
                           bg="#4CAF50", fg="white", font=("Helvetica", 14))
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    display_button = Button(donor_frame, text="Display Donors", command=lambda: display_donors(conn, donor_tree),
                            bg="#008CBA", fg="white", font=("Helvetica", 14))
    display_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Frame for Receivers
    receiver_frame = Frame(root, bg="#e0f7fa")
    receiver_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Labels and Entry Widgets for Receivers
    label_receiver_name = Label(receiver_frame, text="Receiver Name:", bg="#e0f7fa", font=("Helvetica", 14))
    label_receiver_name.grid(row=0, column=0, padx=10, pady=10)
    entry_receiver_name = Entry(receiver_frame, bg="#b2ebf2", font=("Helvetica", 14))
    entry_receiver_name.grid(row=0, column=1, padx=10, pady=10)

    label_blood_group_receiver = Label(receiver_frame, text="Blood Group:", bg="#e0f7fa", font=("Helvetica", 14))
    label_blood_group_receiver.grid(row=1, column=0, padx=10, pady=10)
    blood_group_var_receiver = StringVar()
    blood_group_receiver_combobox = ttk.Combobox(receiver_frame, textvariable=blood_group_var_receiver,
                                                  values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                                  state="readonly", font=("Helvetica", 14))
    blood_group_receiver_combobox.grid(row=1, column=1, padx=10, pady=10)

    label_receiver_contact = Label(receiver_frame, text="Contact Number:", bg="#e0f7fa", font=("Helvetica", 14))
    label_receiver_contact.grid(row=2, column=0, padx=10, pady=10)
    entry_receiver_contact = Entry(receiver_frame, bg="#b2ebf2", font=("Helvetica", 14))
    entry_receiver_contact.grid(row=2, column=1, padx=10, pady=10)

    # Create Treeview for Receivers
    columns_receivers = ("ID", "Name", "Blood Group", "Contact")
    receiver_tree = ttk.Treeview(receiver_frame, columns=columns_receivers, show="headings", height=13)

    # Set column headings
    for col in columns_receivers:
        receiver_tree.heading(col, text=col)
        receiver_tree.column(col, width=170)  # Adjust the width as needed

    # Add a vertical scrollbar
    scrollbar_receivers = ttk.Scrollbar(receiver_frame, orient="vertical", command=receiver_tree.yview)
    receiver_tree.configure(yscrollcommand=scrollbar_receivers.set)

    # Add a horizontal scrollbar
    scrollbar_horizontal_receivers = ttk.Scrollbar(receiver_frame, orient="horizontal", command=receiver_tree.xview)
    receiver_tree.configure(xscrollcommand=scrollbar_horizontal_receivers.set)

    # Grid placement of Treeview and Scrollbars
    receiver_tree.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
    scrollbar_receivers.grid(row=3, column=2, pady=10, sticky="ns")
    scrollbar_horizontal_receivers.grid(row=4, column=0, columnspan=2, sticky="ew")

    # Buttons for Receivers
    submit_button_receiver = Button(receiver_frame, text="Submit Receiver", command=lambda: add_receiver(conn, entry_receiver_name.get(),
                                                                                              blood_group_var_receiver.get(), entry_receiver_contact.get(),
                                                                                              entry_receiver_name, blood_group_receiver_combobox, entry_receiver_contact, receiver_tree),
                                    bg="#FF5733", fg="white", font=("Helvetica", 14))
    submit_button_receiver.grid(row=5, column=0, columnspan=2, pady=10)

    display_button_receiver = Button(receiver_frame, text="Display Receivers", command=lambda: display_receivers(conn, receiver_tree),
                                     bg="#FF8C00", fg="white", font=("Helvetica", 14))
    display_button_receiver.grid(row=6, column=0, columnspan=2, pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: close_application(conn, root))
    root.mainloop()

if __name__ == "__main__":
    main()
