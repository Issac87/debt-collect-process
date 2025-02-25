import sys

def ingest_amounts(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                name, amount = line.strip().split(',')
                amount = float(amount)
                transactions.append((name, amount))
            except ValueError:
                print(f"Invalid input in line: {line.strip()}")
    return transactions

def calculate_balances(transactions):
    balances = {}
    for name, amount in transactions:
        if name in balances:
            balances[name] += amount
        else:
            balances[name] = amount
    return balances

def determine_debts(balances):
    creditors = {name: amount for name, amount in balances.items() if amount > 0}
    debtors = {name: -amount for name, amount in balances.items() if amount < 0}
    return creditors, debtors

def process_debts(creditors, debtors):
    creditor_list = sorted(creditors.items(), key=lambda x: x[1], reverse=True)
    debtor_list = sorted(debtors.items(), key=lambda x: x[1], reverse=True)
    debts_text = ""

    while debtor_list and creditor_list:
        debtor, debt_amount = debtor_list.pop(0)
        for i in range(len(creditor_list)):
            creditor, credit_amount = creditor_list[i]
            if debt_amount == 0:
                break
            payment = min(debt_amount, credit_amount)
            if payment > 0:
                debts_text += f"{debtor} ל-{creditor} {payment:.2f}\n"
                debt_amount -= payment
                creditor_list[i] = (creditor, credit_amount - payment)
                if creditor_list[i][1] == 0:
                    creditor_list.pop(i)
                    break
        if debt_amount > 0:
            debtor_list.append((debtor, debt_amount))

    return debts_text

def process_transactions(transactions):
    balances = calculate_balances(transactions)
    total_balance = sum(balances.values())

    if total_balance not in [0, 1, -1]:
        warning_message = f"אזהרה: היתרה הכוללת של הרווחים וההפסדים היא {total_balance}, שאינה 0, 1 או -1."
    else:
        warning_message = ""

    creditors, debtors = determine_debts(balances)

    balances_text = "יתרות:\n"
    for name, balance in balances.items():
        balances_text += f"{name}: {balance:.2f}\n"

    debts_text = process_debts(creditors, debtors)

    return balances_text, debts_text, warning_message

def run_command_line():
    file_path = "transactions.txt"  # Use relative path
    transactions = ingest_amounts(file_path)
    balances_text, debts_text, warning_message = process_transactions(transactions)

    if warning_message:
        print(warning_message)

    print(balances_text)
    print("\nחובות:")
    print(debts_text)

def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    def load_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            global transactions
            transactions = ingest_amounts(file_path)
            balances_text, debts_text, warning_message = process_transactions(transactions)
            if warning_message:
                messagebox.showwarning("Warning", warning_message)
            result_textbox.delete(1.0, tk.END)
            result_textbox.insert(tk.END, balances_text + "\n\n" + debts_text)

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

    def update_transactions_list():
        transactions_list.delete(0, tk.END)
        for name, amount in transactions:
            transactions_list.insert(tk.END, f"{name}: ₪{amount:.2f}")

    def clear_output():
        result_textbox.delete(1.0, tk.END)
        transactions_list.delete(0, tk.END)
        transactions.clear()

    def copy_to_clipboard():
        app.clipboard_clear()
        debts_only = result_textbox.get(1.0, tk.END).split("\n\n")[1]  # Extract only the debts part
        app.clipboard_append(debts_only)
        messagebox.showinfo("Copied", "Debts information copied to clipboard")

    def process_transactions_ui():
        balances_text, debts_text, warning_message = process_transactions(transactions)
        if warning_message:
            messagebox.showwarning("Warning", warning_message)
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, balances_text + "\n\n" + debts_text)

    app = tk.Tk()
    app.title("Debt Settlement Application")

    transactions = []

    frame = tk.Frame(app, bg="#f0f0f0")
    frame.pack(padx=10, pady=10)

    left_frame = tk.Frame(frame, bg="#f0f0f0")
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = tk.Frame(frame, bg="#f0f0f0")
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    load_button = tk.Button(left_frame, text="Load Transactions File", command=load_file, bg="#add8e6")
    load_button.pack(pady=5)

    name_label = tk.Label(left_frame, text="Name:", fg="#228b22", bg="#f0f0f0")
    name_label.pack(pady=5)
    name_entry = tk.Entry(left_frame)
    name_entry.pack(pady=5)

    amount_label = tk.Label(left_frame, text="Amount:", fg="#228b22", bg="#f0f0f0")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(left_frame)
    amount_entry.pack(pady=5)

    add_button = tk.Button(left_frame, text="Add Transaction", command=add_transaction, bg="#90ee90")
    add_button.pack(pady=5)

    remove_button = tk.Button(left_frame, text="Remove Selected Transaction", command=remove_transaction, bg="#ff6347")
    remove_button.pack(pady=5)

    transactions_list = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, bg="#ffffff", fg="#000000")
    transactions_list.pack(pady=5)

    process_button = tk.Button(left_frame, text="Process Transactions", command=process_transactions_ui, bg="#ffffe0")
    process_button.pack(pady=5)

    clear_button = tk.Button(left_frame, text="Clear", command=clear_output, bg="#d3d3d3")
    clear_button.pack(pady=5)

    copy_button = tk.Button(left_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#add8e6")
    copy_button.pack(pady=5)

    scrollbar = tk.Scrollbar(right_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_textbox = tk.Text(right_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=50, height=20, bg="#ffffe0", fg="#000000")
    result_textbox.pack(pady=5)
    scrollbar.config(command=result_textbox.yview)

    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_gui()
    else:
        run_command_line()
