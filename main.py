"""
Python Banking System - Main Entry Point
Author: Dhiraj Mantri
"""

from bank.account import AccountManager
from bank.auth import AuthManager
from bank.utils import print_header, print_menu, get_input, clear_screen


def main():
    auth = AuthManager()
    manager = AccountManager()

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
            login_flow(manager, auth)

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
    print(" Please save your account number for future login.")


def login_flow(manager, auth):
    print_header("LOGIN TO ACCOUNT")

    acc_num = get_input("Enter account number")
    pin = get_input("Enter PIN")

    account = auth.authenticate(acc_num, pin, manager)
    if not account:
        print(" Invalid account number or PIN!")
        return

    account_menu(manager, account)


def account_menu(manager, account):
    while True:
        clear_screen()
        print_header(f"ACCOUNT: {account.name} | #{account.account_number}")
        print_menu([
            "Check Balance",
            "Deposit Money",
            "Withdraw Money",
            "Transfer Funds",
            "Transaction History",
            "Logout"
        ])

        choice = get_input("Enter choice", default="6")

        if choice == "1":
            print(f"\n Current Balance: ${account.balance:.2f}")

        elif choice == "2":
            deposit_flow(manager, account)

        elif choice == "3":
            withdraw_flow(manager, account)

        elif choice == "4":
            transfer_flow(manager, account)

        elif choice == "5":
            show_history(account)

        elif choice == "6":
            print(" Logged out successfully.")
            break

        input("\n Press Enter to continue...")


def deposit_flow(manager, account):
    amount = get_input("Enter amount to deposit", as_float=True)
    if amount is None or amount <= 0:
        print(" Invalid amount!")
        return

    if manager.deposit(account.account_number, amount):
        print(f" Successfully deposited ${amount:.2f}")
        print(f" New Balance: ${account.balance:.2f}")
    else:
        print(" Deposit failed!")


def withdraw_flow(manager, account):
    amount = get_input("Enter amount to withdraw", as_float=True)
    if amount is None or amount <= 0:
        print(" Invalid amount!")
        return

    if manager.withdraw(account.account_number, amount):
        print(f" Successfully withdrew ${amount:.2f}")
        print(f" New Balance: ${account.balance:.2f}")
    else:
        print(" Insufficient balance or invalid amount!")


def transfer_flow(manager, account):
    target_acc = get_input("Enter recipient account number")
    amount = get_input("Enter amount to transfer", as_float=True)

    if amount is None or amount <= 0:
        print(" Invalid amount!")
        return

    result = manager.transfer(account.account_number, target_acc, amount)
    if result:
        print(f" Successfully transferred ${amount:.2f} to account #{target_acc}")
        print(f" Your New Balance: ${account.balance:.2f}")
    else:
        print(" Transfer failed! Check account number and balance.")


def show_history(account):
    print_header("TRANSACTION HISTORY")
    if not account.transactions:
        print(" No transactions yet.")
        return

    print(f"{'Date':<20} {'Type':<12} {'Amount':>10} {'Balance':>10}")
    print("-" * 56)
    for tx in account.transactions:
        print(f"{tx['date']:<20} {tx['type']:<12} ${tx['amount']:>9.2f} ${tx['balance']:>9.2f}")


def admin_list_accounts(manager):
    print_header("ALL ACCOUNTS (ADMIN VIEW)")
    accounts = manager.get_all_accounts()
    if not accounts:
        print(" No accounts found.")
        return

    print(f"{'Acc #':<10} {'Name':<20} {'Balance':>12}")
    print("-" * 46)
    for acc in accounts:
        print(f"{acc.account_number:<10} {acc.name:<20} ${acc.balance:>11.2f}")


if __name__ == "__main__":
    main()
