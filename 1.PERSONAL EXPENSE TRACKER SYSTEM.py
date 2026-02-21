import tkinter as tk
from tkinter import ttk, messagebox
import csv
import json
from datetime import datetime
import os

CSV_FILE = "expenses.csv"
JSON_FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("750x500")

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        # Input Frame
        frame = ttk.LabelFrame(self.root, text="Add Expense")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
        ttk.Label(frame, text="Category").grid(row=0, column=1)
        ttk.Label(frame, text="Description").grid(row=0, column=2)
        ttk.Label(frame, text="Amount").grid(row=0, column=3)

        self.date_entry = ttk.Entry(frame)
        self.category_entry = ttk.Entry(frame)
        self.desc_entry = ttk.Entry(frame)
        self.amount_entry = ttk.Entry(frame)

        self.date_entry.grid(row=1, column=0, padx=5)
        self.category_entry.grid(row=1, column=1, padx=5)
        self.desc_entry.grid(row=1, column=2, padx=5)
        self.amount_entry.grid(row=1, column=3, padx=5)

        ttk.Button(frame, text="Add Expense", command=self.add_expense)\
            .grid(row=1, column=4, padx=5)

        # Table
        columns = ("Date", "Category", "Description", "Amount")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_expense).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Monthly Summary", command=self.monthly_summary).pack(side="left", padx=5)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()
        amount = self.amount_entry.get()

        if not date or not category or not amount:
            messagebox.showerror("Error", "Please fill required fields")
            return

        try:
            float(amount)
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or amount")
            return

        self.tree.insert("", "end", values=(date, category, desc, amount))
        self.save_expenses()

        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            self.tree.delete(item)
        self.save_expenses()

    def save_expenses(self):
        data = []
        for row in self.tree.get_children():
            data.append(self.tree.item(row)["values"])

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Description", "Amount"])
            writer.writerows(data)

        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_expenses(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.tree.insert("", "end", values=row)

    def monthly_summary(self):
        summary = {}
        for row in self.tree.get_children():
            date, category, _, amount = self.tree.item(row)["values"]
            month = date[:7]
            summary[month] = summary.get(month, 0) + float(amount)

        result = "\n".join(f"{m}: ₹{a:.2f}" for m, a in summary.items())
        messagebox.showinfo("Monthly Summary", result or "No data")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
