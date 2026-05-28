"""
Python Banking System - CLI Entry Point
Author: Dhiraj Mantri
"""

from bank.account import AccountManager
from bank.auth import AuthManager
from bank.loan import LoanManager
from bank.utils import print_header, print_menu, get_input, clear_screen


def main():
    auth = AuthManager()
    manager = AccountManager()
    loan_manager = LoanManager()

    while True:
        clear_screen()
        print_header("WELCOME TO PYTHON BANKING SYSTEM")
        print_menu([
            "Create New Account",
            "Login to Account",
            "Admin: List All Accounts",
            "Exit"
        ])

        choice = get_input("Enter choice", default="4")

        if choice == "1":
            create_account_flow(manager, auth)
        elif choice == "2":
            login_flow(manager, auth, loan_manager)
        elif choice == "3":
            admin_list_accounts(manager)
        elif choice == "4":
            print("\n Thank you for using Python Banking System!")
            break

        input("\n Press Enter to continue...")


def create_account_flow(manager, auth):
    print_header("CREATE NEW ACCOUNT")
    name = get_input("Enter your full name")
    if not name:
        print(" Name cannot be empty!")
        return
    initial_deposit = get_input("Enter initial deposit amount", as_float=True)
    if initial_deposit is None or initial_deposit < 0:
        print(" Invalid deposit amount!")
        return
    pin = get_input("Set a 4-digit PIN", default="1234")
    if not pin.isdigit() or len(pin) != 4:
        print(" PIN must be exactly 4 digits!")
        return
    account = manager.create_account(name, initial_deposit, pin)
    print(f"\n Account created successfully!")
    print(f" Account Number: {account.account_number}")
    print(f" Account Holder: {account.name}")
    print(f" Current Balance: ${account.balance:.2f}")


def login_flow(manager, auth, loan_manager):
    print_header("LOGIN TO ACCOUNT")
    acc_num = get_input("Enter account number")
    pin = get_input("Enter PIN")
    account = auth.authenticate(acc_num, pin, manager)
    if not account:
        print(" Invalid account number or PIN!")
        return
    account_menu(manager, account, loan_manager)


def account_menu(manager, account, loan_manager):
    while True:
        clear_screen()
        print_header(f"ACCOUNT: {account.name} | #{account.account_number}")
        print_menu([
            "Check Balance",
            "Deposit Money",
            "Withdraw Money",
            "Transfer Funds",
            "Calculate & Credit Interest",
            "Loan Management",
            "Transaction History",
            "Logout"
        ])
        choice = get_input("Enter choice", default="8")
        if choice == "1":
            print(f"\n Balance: ${account.balance:.2f}")
        elif choice == "2":
            deposit_flow(manager, account)
        elif choice == "3":
            withdraw_flow(manager, account)
        elif choice == "4":
            transfer_flow(manager, account)
        elif choice == "5":
            interest_flow(manager, account)
        elif choice == "6":
            loan_menu(manager, account, loan_manager)
        elif choice == "7":
            show_history(account)
        elif choice == "8":
            print(" Logged out.")
            break
        input("\n Press Enter to continue...")


def deposit_flow(manager, account):
    amount = get_input("Enter amount to deposit", as_float=True)
    if amount and amount > 0 and manager.deposit(account.account_number, amount):
        print(f" Deposited ${amount:.2f}")
    else:
        print(" Deposit failed!")


def withdraw_flow(manager, account):
    amount = get_input("Enter amount to withdraw", as_float=True)
    if amount and amount > 0 and manager.withdraw(account.account_number, amount):
        print(f" Withdrew ${amount:.2f}")
    else:
        print(" Withdrawal failed!")


def transfer_flow(manager, account):
    target = get_input("Enter recipient account number")
    amount = get_input("Enter amount", as_float=True)
    if amount and amount > 0 and manager.transfer(account.account_number, target, amount):
        print(f" Transferred ${amount:.2f}")
    else:
        print(" Transfer failed!")


def interest_flow(manager, account):
    months = get_input("Enter months", as_float=True)
    if months and months > 0:
        preview = manager.calculate_interest_preview(account.account_number, int(months))
        if preview:
            print(f" Interest: ${preview['interest']:.2f}")
            if get_input("Credit? (y/n)", default="n").lower() == "y":
                manager.credit_interest(account.account_number, int(months))
                print(" Credited!")


def loan_menu(manager, account, loan_manager):
    while True:
        clear_screen()
        print_header("LOAN MANAGEMENT")
        print_menu([
            "Apply for New Loan",
            "View My Loans",
            "EMI Calculator",
            "Repay Loan EMI",
            "Back"
        ])
        choice = get_input("Enter choice", default="5")
        if choice == "1":
            apply_loan_flow(manager, account, loan_manager)
        elif choice == "2":
            for loan in loan_manager.get_loans_by_account(account.account_number):
                print(f" {loan['loan_id']}: ${loan['remaining_amount']:.2f} remaining")
        elif choice == "3":
            p = get_input("Principal", as_float=True)
            r = get_input("Rate %", as_float=True)
            n = get_input("Months", as_float=True)
            if p and r and n:
                emi = LoanManager.calculate_emi(p, r/100, int(n))
                print(f" EMI: ${emi:.2f}")
        elif choice == "4":
            loans = loan_manager.get_active_loans(account.account_number)
            for i, loan in enumerate(loans, 1):
                print(f" [{i}] {loan['loan_id']} - EMI ${loan['emi']:.2f}")
            choice = get_input("Select", as_float=True)
            if choice and 1 <= int(choice) <= len(loans):
                loan = loans[int(choice)-1]
                if manager.withdraw(account.account_number, loan["emi"]):
                    loan_manager.repay_emi(loan["loan_id"], loan["emi"])
                    print(" EMI paid!")
        elif choice == "5":
            break
        input("\n Press Enter...")


def apply_loan_flow(manager, account, loan_manager):
    amount = get_input("Loan amount", as_float=True)
    tenure = get_input("Tenure (12-60 months)", as_float=True)
    if amount and tenure and 12 <= tenure <= 60:
        emi = loan_manager.calculate_emi(amount, 0.10, int(tenure))
        print(f" EMI: ${emi:.2f}")
        if get_input("Apply? (y/n)", default="n").lower() == "y":
            loan = loan_manager.apply_loan(account.account_number, amount, 0.10, int(tenure))
            if loan:
                manager.deposit(account.account_number, amount)
                account.add_transaction("LOAN CREDIT", amount)
                manager._save()
                print(f" Loan {loan['loan_id']} approved!")


def show_history(account):
    print_header("TRANSACTION HISTORY")
    for tx in account.transactions:
        print(f" {tx['date']} | {tx['type']:<18} | ${tx['amount']:>9.2f}")


def admin_list_accounts(manager):
    print_header("ALL ACCOUNTS")
    for acc in manager.get_all_accounts():
        print(f" {acc.account_number} | {acc.name:<20} | ${acc.balance:>11.2f}")


if __name__ == "__main__":
    main()
