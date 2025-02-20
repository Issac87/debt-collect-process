import tkinter as tk
from tkinter import filedialog, messagebox
from ingest_amounts import ingest_amounts, calculate_balances, determine_debts
import pytesseract
from PIL import Image

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        transactions = ingest_amounts(file_path)
        process_transactions(transactions)

def add_transaction():
    name = name_entry.get()
    amount = amount_entry.get()
    try:
        amount = float(amount)
        transactions.append((name, amount))
        name_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        update_transactions_list()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")

def remove_transaction():
    selected_indices = transactions_list.curselection()
    if selected_indices:
        for index in selected_indices[::-1]:
            transactions.pop(index)
        update_transactions_list()
    else:
        messagebox.showerror("Error", "No transaction selected. Please select a transaction to remove.")

def process_transactions(transactions):
    balances = calculate_balances(transactions)
    total_balance = sum(balances.values())

    if total_balance not in [0, 1, -1]:
        messagebox.showwarning("Warning", f"אזהרה: היתרה הכוללת של הרווחים וההפסדים היא {total_balance}, שאינה 0, 1 או -1.")

    creditors, debtors = determine_debts(balances)

    balances_text = "יתרות:\n"
    for name, balance in balances.items():
        balances_text += f"{name}: ₪{balance:.2f}\n"

    debts_text = "\nחובות:\n"
    creditor_list = sorted(creditors.items(), key=lambda x: x[1], reverse=True)
    debtor_list = sorted(debtors.items(), key=lambda x: x[1], reverse=True)

    for debtor, debt_amount in debtor_list:
        for i in range(len(creditor_list)):
            creditor, credit_amount = creditor_list[i]
            if debt_amount == 0:
                break
            payment = min(debt_amount, credit_amount)
            if payment > 0:
                debts_text += f"{debtor} חייב ל-{creditor} ₪{payment:.2f}\n"
                debt_amount -= payment
                creditor_list[i] = (creditor, credit_amount - payment)
                if creditor_list[i][1] == 0:
                    creditor_list.pop(i)
                    break
        debtor_list = [(d, da) if d != debtor else (d, debt_amount) for d, da in debtor_list]

    for debtor, debt_amount in debtor_list:
        if debt_amount > 0:
            for i in range(len(creditor_list)):
                creditor, credit_amount = creditor_list[i]
                if debt_amount == 0:
                    break
                payment = min(debt_amount, credit_amount)
                if payment > 0:
                    debts_text += f"{debtor} חייב ל-{creditor} ₪{payment:.2f}\n"
                    debt_amount -= payment
                    creditor_list[i] = (creditor, credit_amount - payment)
                    if creditor_list[i][1] == 0:
                        creditor_list.pop(i)
                        break
            debtor_list = [(d, da) if d != debtor else (d, debt_amount) for d, da in debtor_list]

    result_text.set(balances_text + debts_text)

def update_transactions_list():
    transactions_list.delete(0, tk.END)
    for name, amount in transactions:
        transactions_list.insert(tk.END, f"{name}: ₪{amount:.2f}")

def clear_output():
    result_text.set("")
    transactions_list.delete(0, tk.END)
    transactions.clear()

def read_from_screenshot():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png"), ("Image files", "*.jpg"), ("Image files", "*.jpeg")])
    if file_path:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            lines = text.split('\n')
            for line in lines:
                if ',' in line:
                    name, amount = line.split(',')
                    try:
                        amount = float(amount)
                        transactions.append((name.strip(), amount))
                    except ValueError:
                        continue
            update_transactions_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read from screenshot: {e}")

app = tk.Tk()
app.title("Debt Settlement Application")

transactions = []

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

load_button = tk.Button(frame, text="Load Transactions File", command=load_file)
load_button.pack(pady=5)

name_label = tk.Label(frame, text="Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(frame)
name_entry.pack(pady=5)

amount_label = tk.Label(frame, text="Amount:")
amount_label.pack(pady=5)
amount_entry = tk.Entry(frame)
amount_entry.pack(pady=5)

add_button = tk.Button(frame, text="Add Transaction", command=add_transaction)
add_button.pack(pady=5)

remove_button = tk.Button(frame, text="Remove Selected Transaction", command=remove_transaction)
remove_button.pack(pady=5)

transactions_list = tk.Listbox(frame, selectmode=tk.MULTIPLE)
transactions_list.pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify="left")
result_label.pack(pady=5)

process_button = tk.Button(frame, text="Process Transactions", command=lambda: process_transactions(transactions))
process_button.pack(pady=5)

clear_button = tk.Button(frame, text="Clear", command=clear_output)
clear_button.pack(pady=5)

ocr_button = tk.Button(frame, text="Read from Screenshot", command=read_from_screenshot)
ocr_button.pack(pady=5)

app.mainloop()
