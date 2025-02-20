# Debt Settlement Script

This script helps to settle debts between multiple people by calculating who owes whom and how much. It reads a list of transactions from a file, calculates the balances for each person, and then determines the debts and credits.

## How to Use

### Command Line Interface

1. **Prepare the Transactions File:**
   - Create a file named `transactions.txt` in the same directory as the script.
   - Each line in the file should contain a name and an amount, separated by a comma.
   - Positive amounts represent credits (money given), and negative amounts represent debts (money owed).
   - Example:
     ```
     vova,1000
     itzhak,500
     yan,400
     shlomi,-600
     asher,-1200
     oren,-100
     ```

2. **Run the Script:**
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using Python:
     ```
     python ingest_amounts.py
     ```

3. **View the Results:**
   - The script will print the balances for each person.
   - It will also print the debts and credits, showing who owes whom and how much.

### Graphical User Interface

1. **Prepare the Transactions File:**
   - Create a file named `transactions.txt` in any location.
   - Each line in the file should contain a name and an amount, separated by a comma.
   - Positive amounts represent credits (money given), and negative amounts represent debts (money owed).
   - Example:
     ```
     וובה,1000
     יצחק,500
     יאן,400
     שלומי,-600
     אשר,-1200
     אורן,-100
     ```

2. **Install Required Dependencies:**
   - Open a terminal and run the following commands:
     ```sh
     pip install pytesseract pillow
     brew install tesseract
     ```

3. **Run the GUI Application:**
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using Python with the `--gui` option:
     ```
     python ingest_amounts.py --gui
     ```

4. **Load the Transactions File:**
   - Click the "Load Transactions File" button.
   - Select the `transactions.txt` file from the file dialog.

5. **Read from Screenshot:**
   - Click the "Read from Screenshot" button.
   - Select an image file containing the transactions.

6. **View the Results:**
   - The application will display the balances for each person.
   - It will also display the debts and credits, showing who owes whom and how much.

## Example Output

```
Balances:
vova: $1000.00
itzhak: $500.00
yan: $400.00
shlomi: $-600.00
asher: $-1200.00
oren: $-100.00
roy: $-50.00
maxim: $100.00
shai: $-50.00

Debts:
asher owes vova $1000.00
shlomi owes itzhak $500.00
oren owes yan $100.00
roy owes yan $50.00
shai owes yan $50.00
asher owes yan $200.00
shlomi owes maxim $100.00
```

## Notes

- The script assumes that the total balance of all transactions should be 0, 1, or -1. If it is not, a warning will be printed.
- Make sure the `transactions.txt` file is formatted correctly to avoid errors.

Enjoy using the debt settlement script!

