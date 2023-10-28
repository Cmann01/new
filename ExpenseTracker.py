import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from tkinter import messagebox
import csv

# Function to add an expense record to the database
def add_expense():
    date, category, amount, description = date_entry.get(), category_entry.get(), amount_entry.get(), description_entry.get()

    if date and category and amount:
        try:
            cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                           (date, category, amount, description))
            conn.commit()
            clear_input_fields()
            messagebox.showinfo("Success", "Expense added successfully.")
        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error adding expense: {e}")
    else:
        messagebox.showerror("Error", "Date, Category, and Amount are required fields.")

# Function to clear input fields
def clear_input_fields():
    for entry in [date_entry, category_entry, amount_entry, description_entry]:
        entry.delete(0, tk.END)

# Function to retrieve and display all stored expenses
def display_expenses():
    try:
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

        if data:
            # Create a new window to display the expenses
            display_window = tk.Toplevel(app)
            display_window.title('Expense History')

            # Create a text widget to display the expenses
            display_text = tk.Text(display_window, wrap=tk.WORD)
            display_text.pack()

            # Insert the expenses data into the text widget
            for expense in data:
                display_text.insert(tk.END, f"Date: {expense[1]}\n")
                display_text.insert(tk.END, f"Category: {expense[2]}\n")
                display_text.insert(tk.END, f"Amount: {expense[3]}\n")
                display_text.insert(tk.END, f"Description: {expense[4]}\n\n")

            # Make the text widget read-only
            display_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Info", "No expenses found in the database.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")

# Function to export expenses to a CSV file
def export_to_csv():
    try:
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

        if data:
            with open('expenses.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Date', 'Category', 'Amount', 'Description'])
                csv_writer.writerows(data)
            messagebox.showinfo("Info", "Expenses exported to 'expenses.csv' successfully.")
        else:
            messagebox.showinfo("Info", "No expenses found to export.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")

def on_close():
    conn.close()
    app.destroy()

# Create the main window
app = tk.Tk()
app.title('Expense Tracker')
app.geometry("800x500")  # Larger window size

# Create and configure a frame to contain the input fields
input_frame = tk.Frame(app, padx=10, pady=10)
input_frame.pack()

labels = ['Date', 'Category', 'Amount', 'Description']
entries = []

for label in labels:
    label_widget = tk.Label(input_frame, text=label + ":")
    label_widget.grid(row=labels.index(label), column=0, sticky='w', padx=5, pady=5)
    entry = tk.Entry(input_frame, width=30)  # Wider input fields
    entry.grid(row=labels.index(label), column=1, padx=5, pady=5)
    entries.append(entry)

# Assign the global input field variables
date_entry = entries[0]
category_entry = entries[1]
amount_entry = entries[2]
description_entry = entries[3]

# Create a colorful title label
title_label = tk.Label(app, text='Expense Tracker', font=("Helvetica", 20), bg='blue', fg='white', padx=10, pady=10)
title_label.pack(fill='x')

# Create the Add Expense button with a colorful design
add_button = tk.Button(app, text='Add Expense', command=add_expense, bg='green', fg='white', padx=10, pady=5)
add_button.pack()

# Create buttons for displaying expenses and exporting to CSV with colorful design
display_button = tk.Button(app, text='Display Expenses', command=display_expenses, bg='orange', fg='white', padx=10, pady=5)
display_button.pack()
export_button = tk.Button(app, text='Export to CSV', command=export_to_csv, bg='red', fg='white', padx=10, pady=5)
export_button.pack()

# Rest of the code (month/year selection, report generation, database setup) remains the same

app.protocol("WM_DELETE_WINDOW", on_close)

# Create or connect to the SQLite database
try:
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   date DATE, 
                   category TEXT, 
                   amount REAL, 
                   description TEXT)''')
    conn.commit()
except sqlite3.Error as e:
    messagebox.showerror("Database Error", f"Error connecting to database: {e}")

app.mainloop()
