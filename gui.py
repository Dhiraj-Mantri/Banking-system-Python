"""
Python Banking System - Tkinter GUI
Author: Dhiraj Mantri
Version: 4.0 - Desktop GUI Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bank.account import AccountManager
from bank.auth import AuthManager
from bank.loan import LoanManager


class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Banking System - v4.0")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        self.manager = AccountManager()
        self.auth = AuthManager()
        self.loan_manager = LoanManager()
        self.current_account = None

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 11), padding=6)
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"))

        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ========== LOGIN SCREEN ==========
    def show_login_screen(self):
        self.clear_window()
        self.root.geometry("500x400")

        frame = ttk.Frame(self.root, padding="40")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="🏦 Python Banking System", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(frame, text="v4.0 - Desktop GUI", foreground="gray").pack(pady=(0, 30))

        ttk.Label(frame, text="Account Number:").pack(anchor="w")
        self.acc_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
        self.acc_entry.pack(pady=(0, 15), fill="x")

        ttk.Label(frame, text="PIN:").pack(anchor="w")
        self.pin_entry = ttk.Entry(frame, width=30, font=("Arial", 12), show="*")
        self.pin_entry.pack(pady=(0, 25), fill="x")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Login", command=self.login).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Create Account", command=self.show_create_account).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def login(self):
        acc_num = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not acc_num or not pin:
            messagebox.showerror("Error", "Please enter both account number and PIN")
            return

        account = self.auth.authenticate(acc_num, pin, self.manager)
        if account:
            self.current_account = account
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid account number or PIN")

    # ========== CREATE ACCOUNT ==========
    def show_create_account(self):
        self.clear_window()
        self.root.geometry("500x500")

        frame = ttk.Frame(self.root, padding="40")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Create New Account", style="Header.TLabel").pack(pady=(0, 20))

        ttk.Label(frame, text="Full Name:").pack(anchor="w")
        self.new_name = ttk.Entry(frame, width=30, font=("Arial", 12))
        self.new_name.pack(pady=(0, 10), fill="x")

        ttk.Label(frame, text="Initial Deposit ($):").pack(anchor="w")
        self.new_deposit = ttk.Entry(frame, width=30, font=("Arial", 12))
        self.new_deposit.pack(pady=(0, 10), fill="x")

        ttk.Label(frame, text="4-Digit PIN:").pack(anchor="w")
        self.new_pin = ttk.Entry(frame, width=30, font=("Arial", 12), show="*")
        self.new_pin.pack(pady=(0, 20), fill="x")

        ttk.Button(frame, text="Create Account", command=self.create_account).pack(fill="x", pady=(0, 10))
        ttk.Button(frame, text="Back to Login", command=self.show_login_screen).pack(fill="x")

    def create_account(self):
        name = self.new_name.get().strip()
        deposit_str = self.new_deposit.get().strip()
        pin = self.new_pin.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        try:
            deposit = float(deposit_str) if deposit_str else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid deposit amount")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be exactly 4 digits")
            return

        account = self.manager.create_account(name, deposit, pin)
        messagebox.showinfo("Success", 
            f"Account created!\n\nAccount Number: {account.account_number}\n"
            f"Name: {account.name}\nBalance: ${account.balance:.2f}\n\n"
            f"Please save your account number!")
        self.show_login_screen()

    # ========== DASHBOARD ==========
    def show_dashboard(self):
        self.clear_window()
        self.root.geometry("900x650")

        # Header
        header = ttk.Frame(self.root, padding="15")
        header.pack(fill="x")

        ttk.Label(header, text=f"Welcome, {self.current_account.name}", 
                  style="Header.TLabel").pack(side="left")
        ttk.Label(header, text=f"Account: #{self.current_account.account_number}", 
                  foreground="gray").pack(side="left", padx=(15, 0))
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right")

        ttk.Separator(self.root, orient="horizontal").pack(fill="x")

        # Balance Card
        balance_frame = ttk.LabelFrame(self.root, text="Account Overview", padding="15")
        balance_frame.pack(fill="x", padx=20, pady=15)

        ttk.Label(balance_frame, text=f"Balance: ${self.current_account.balance:,.2f}",
                  font=("Arial", 18, "bold"), foreground="#2e7d32").pack(side="left")

        if self.current_account.total_interest_earned > 0:
            ttk.Label(balance_frame, 
                      text=f"Interest Earned: ${self.current_account.total_interest_earned:,.2f}",
                      foreground="#1565c0").pack(side="right")

        # Buttons Grid
        btn_frame = ttk.Frame(self.root, padding="15")
        btn_frame.pack(fill="both", expand=True, padx=20)

        buttons = [
            ("💰 Deposit", self.show_deposit),
            ("💸 Withdraw", self.show_withdraw),
            ("🔄 Transfer", self.show_transfer),
            ("📈 Interest", self.show_interest),
            ("🏦 Loans", self.show_loan_menu),
            ("📜 History", self.show_history),
        ]

        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            btn = tk.Button(btn_frame, text=text, command=cmd, font=("Arial", 13),
                           bg="#1976d2", fg="white", width=18, height=3,
                           activebackground="#1565c0", cursor="hand2")
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for i in range(3):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(2):
            btn_frame.rowconfigure(i, weight=1)

    def logout(self):
        self.current_account = None
        self.show_login_screen()

    # ========== DEPOSIT ==========
    def show_deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:", 
                                        minvalue=0.01, parent=self.root)
        if amount:
            if self.manager.deposit(self.current_account.account_number, amount):
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}\nNew Balance: ${self.current_account.balance:.2f}")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Deposit failed")

    # ========== WITHDRAW ==========
    def show_withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:", 
                                        minvalue=0.01, parent=self.root)
        if amount:
            if self.manager.withdraw(self.current_account.account_number, amount):
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}\nNew Balance: ${self.current_account.balance:.2f}")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Insufficient balance or invalid amount")

    # ========== TRANSFER ==========
    def show_transfer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Transfer Funds")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Transfer Funds", style="Header.TLabel").pack(pady=15)

        ttk.Label(dialog, text="Recipient Account Number:").pack(anchor="w", padx=20)
        target_entry = ttk.Entry(dialog, width=35, font=("Arial", 12))
        target_entry.pack(padx=20, pady=(0, 10), fill="x")

        ttk.Label(dialog, text="Amount ($):").pack(anchor="w", padx=20)
        amount_entry = ttk.Entry(dialog, width=35, font=("Arial", 12))
        amount_entry.pack(padx=20, pady=(0, 20), fill="x")

        def do_transfer():
            target = target_entry.get().strip()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid amount", parent=dialog)
                return

            if self.manager.transfer(self.current_account.account_number, target, amount):
                messagebox.showinfo("Success", f"Transferred ${amount:.2f} to #{target}", parent=dialog)
                dialog.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Transfer failed! Check account and balance.", parent=dialog)

        ttk.Button(dialog, text="Transfer", command=do_transfer).pack(fill="x", padx=20, pady=(0, 5))
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(fill="x", padx=20)

    # ========== INTEREST ==========
    def show_interest(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Interest Calculator")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Interest Calculator", style="Header.TLabel").pack(pady=15)
        ttk.Label(dialog, text=f"Current Balance: ${self.current_account.balance:.2f}").pack()
        ttk.Label(dialog, text=f"Rate: {self.manager.INTEREST_RATE*100:.1f}% per annum").pack(pady=(0, 15))

        ttk.Label(dialog, text="Number of months:").pack(anchor="w", padx=20)
        months_var = tk.StringVar(value="12")
        months_entry = ttk.Entry(dialog, textvariable=months_var, width=35, font=("Arial", 12))
        months_entry.pack(padx=20, pady=(0, 15), fill="x")

        result_frame = ttk.LabelFrame(dialog, text="Preview", padding="10")
        result_frame.pack(fill="x", padx=20, pady=10)

        result_label = ttk.Label(result_frame, text="Enter months and click Preview", 
                                  font=("Arial", 11))
        result_label.pack()

        def preview():
            try:
                months = int(months_var.get())
                if months <= 0:
                    raise ValueError
            except ValueError:
                result_label.config(text="Invalid months", foreground="red")
                return

            preview_data = self.manager.calculate_interest_preview(
                self.current_account.account_number, months)
            if preview_data:
                result_label.config(
                    text=f"Interest: ${preview_data['interest']:.2f}\n"
                         f"New Balance: ${preview_data['new_balance']:.2f}",
                    foreground="#2e7d32"
                )

        def credit():
            try:
                months = int(months_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid months", parent=dialog)
                return

            if self.manager.credit_interest(self.current_account.account_number, months):
                messagebox.showinfo("Success", 
                    f"Interest credited!\nNew Balance: ${self.current_account.balance:.2f}",
                    parent=dialog)
                dialog.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Failed to credit interest", parent=dialog)

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", padx=20, pady=10)
        ttk.Button(btn_frame, text="Preview", command=preview).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Credit to Account", command=credit).pack(side="right", expand=True, fill="x", padx=(5, 0))
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(fill="x", padx=20)

    # ========== LOAN MENU ==========
    def show_loan_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Loan Management")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Loan Management", style="Header.TLabel").pack(pady=15)

        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab 1: Apply
        apply_tab = ttk.Frame(notebook, padding="15")
        notebook.add(apply_tab, text="Apply Loan")

        ttk.Label(apply_tab, text="Loan Amount ($):").pack(anchor="w")
        loan_amount = ttk.Entry(apply_tab, font=("Arial", 12))
        loan_amount.pack(fill="x", pady=(0, 10))

        ttk.Label(apply_tab, text="Tenure (months, 12-60):").pack(anchor="w")
        loan_tenure = ttk.Entry(apply_tab, font=("Arial", 12))
        loan_tenure.pack(fill="x", pady=(0, 10))

        preview_label = ttk.Label(apply_tab, text="", font=("Arial", 11))
        preview_label.pack(pady=10)

        def calc_emi():
            try:
                p = float(loan_amount.get())
                n = int(loan_tenure.get())
                if n < 12 or n > 60:
                    raise ValueError
            except ValueError:
                preview_label.config(text="Invalid input", foreground="red")
                return

            emi = self.loan_manager.calculate_emi(p, 0.10, n)
            total = emi * n
            preview_label.config(
                text=f"EMI: ${emi:.2f}/month\nTotal Interest: ${total-p:.2f}\nTotal Payable: ${total:.2f}",
                foreground="#1565c0"
            )

        def apply_loan():
            try:
                p = float(loan_amount.get())
                n = int(loan_tenure.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid input", parent=dialog)
                return

            max_loan = self.current_account.balance * 5
            if p > max_loan:
                messagebox.showerror("Error", f"Max eligible: ${max_loan:.2f}", parent=dialog)
                return

            loan = self.loan_manager.apply_loan(self.current_account.account_number, p, 0.10, n)
            if loan:
                self.manager.deposit(self.current_account.account_number, p)
                self.current_account.add_transaction("LOAN CREDIT", p)
                self.manager._save()
                messagebox.showinfo("Success", 
                    f"Loan approved!\nID: {loan['loan_id']}\nAmount: ${p:.2f} credited",
                    parent=dialog)
                dialog.destroy()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Loan application failed", parent=dialog)

        ttk.Button(apply_tab, text="Calculate EMI", command=calc_emi).pack(fill="x", pady=(0, 5))
        ttk.Button(apply_tab, text="Apply Loan", command=apply_loan).pack(fill="x")

        # Tab 2: My Loans
        view_tab = ttk.Frame(notebook, padding="15")
        notebook.add(view_tab, text="My Loans")

        columns = ("Loan ID", "Principal", "EMI", "Paid", "Remaining", "Status")
        tree = ttk.Treeview(view_tab, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        loans = self.loan_manager.get_loans_by_account(self.current_account.account_number)
        for loan in loans:
            tree.insert("", "end", values=(
                loan["loan_id"],
                f"${loan['principal']:.2f}",
                f"${loan['emi']:.2f}",
                f"${loan['total_paid']:.2f}",
                f"${loan['remaining_amount']:.2f}",
                loan["status"].upper()
            ))

        # Tab 3: Repay
        repay_tab = ttk.Frame(notebook, padding="15")
        notebook.add(repay_tab, text="Repay EMI")

        active_loans = self.loan_manager.get_active_loans(self.current_account.account_number)

        if not active_loans:
            ttk.Label(repay_tab, text="No active loans to repay", font=("Arial", 12)).pack(pady=50)
        else:
            ttk.Label(repay_tab, text="Select loan to repay EMI:").pack(anchor="w")

            loan_var = tk.StringVar()
            for loan in active_loans:
                text = f"{loan['loan_id']} - EMI: ${loan['emi']:.2f} - Remaining: ${loan['remaining_amount']:.2f}"
                ttk.Radiobutton(repay_tab, text=text, variable=loan_var, 
                               value=loan["loan_id"]).pack(anchor="w", pady=5)

            def do_repay():
                loan_id = loan_var.get()
                if not loan_id:
                    messagebox.showerror("Error", "Select a loan", parent=dialog)
                    return

                loan = self.loan_manager.get_loan(loan_id)
                emi = loan["emi"]

                if self.current_account.balance < emi:
                    messagebox.showerror("Error", "Insufficient balance", parent=dialog)
                    return

                if self.manager.withdraw(self.current_account.account_number, emi):
                    result = self.loan_manager.repay_emi(loan_id, emi)
                    if result:
                        msg = f"EMI ${emi:.2f} paid!"
                        if result["status"] == "paid":
                            msg += "\n\nLoan fully repaid! 🎉"
                        messagebox.showinfo("Success", msg, parent=dialog)
                        dialog.destroy()
                        self.show_dashboard()
                else:
                    messagebox.showerror("Error", "Payment failed", parent=dialog)

            ttk.Button(repay_tab, text="Pay EMI", command=do_repay).pack(fill="x", pady=20)

    # ========== HISTORY ==========
    def show_history(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Transaction History")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Transaction History", style="Header.TLabel").pack(pady=15)

        columns = ("Date", "Type", "Amount", "Balance")
        tree = ttk.Treeview(dialog, columns=columns, show="headings", height=15)

        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Balance", text="Balance")

        tree.column("Date", width=150)
        tree.column("Type", width=150)
        tree.column("Amount", width=100)
        tree.column("Balance", width=100)

        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 15))

        for tx in reversed(self.current_account.transactions):
            tree.insert("", "end", values=(
                tx["date"],
                tx["type"],
                f"${tx['amount']:.2f}",
                f"${tx['balance']:.2f}"
            ))

        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)


def main():
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
