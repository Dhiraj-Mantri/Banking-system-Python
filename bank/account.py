"""
Account Manager - Core banking operations with Interest Calculation
"""

import random
from datetime import datetime
from .storage import Storage


class Account:
    def __init__(self, account_number, name, balance, pin, transactions=None, total_interest_earned=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.pin = pin
        self.transactions = transactions or []
        self.total_interest_earned = total_interest_earned

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "balance": self.balance,
            "pin": self.pin,
            "transactions": self.transactions,
            "total_interest_earned": self.total_interest_earned
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            account_number=data["account_number"],
            name=data["name"],
            balance=data["balance"],
            pin=data["pin"],
            transactions=data.get("transactions", []),
            total_interest_earned=data.get("total_interest_earned", 0.0)
        )

    def add_transaction(self, tx_type, amount):
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": tx_type,
            "amount": amount,
            "balance": self.balance
        })


class AccountManager:
    INTEREST_RATE = 0.04  # 4% per annum

    def __init__(self):
        self.storage = Storage()
        self.accounts = {}
        self._load_accounts()

    def _load_accounts(self):
        data = self.storage.load()
        for acc_num, acc_data in data.items():
            self.accounts[acc_num] = Account.from_dict(acc_data)

    def _save(self):
        data = {k: v.to_dict() for k, v in self.accounts.items()}
        self.storage.save(data)

    def _generate_account_number(self):
        while True:
            num = str(random.randint(100000, 999999))
            if num not in self.accounts:
                return num

    def create_account(self, name, initial_deposit, pin):
        acc_num = self._generate_account_number()
        account = Account(acc_num, name, initial_deposit, pin)
        if initial_deposit > 0:
            account.add_transaction("OPENING", initial_deposit)
        self.accounts[acc_num] = account
        self._save()
        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def get_all_accounts(self):
        return list(self.accounts.values())

    def deposit(self, account_number, amount):
        account = self.accounts.get(account_number)
        if not account or amount <= 0:
            return False
        account.balance += amount
        account.add_transaction("DEPOSIT", amount)
        self._save()
        return True

    def withdraw(self, account_number, amount):
        account = self.accounts.get(account_number)
        if not account or amount <= 0 or amount > account.balance:
            return False
        account.balance -= amount
        account.add_transaction("WITHDRAW", amount)
        self._save()
        return True

    def transfer(self, from_acc_num, to_acc_num, amount):
        if from_acc_num == to_acc_num:
            return False
        from_acc = self.accounts.get(from_acc_num)
        to_acc = self.accounts.get(to_acc_num)
        if not from_acc or not to_acc or amount <= 0 or amount > from_acc.balance:
            return False
        from_acc.balance -= amount
        from_acc.add_transaction(f"TRANSFER TO {to_acc_num}", amount)
        to_acc.balance += amount
        to_acc.add_transaction(f"TRANSFER FROM {from_acc_num}", amount)
        self._save()
        return True

    def calculate_interest_preview(self, account_number, months):
        account = self.accounts.get(account_number)
        if not account or months <= 0:
            return None
        principal = account.balance
        time_years = months / 12
        interest = principal * self.INTEREST_RATE * time_years
        return {
            "principal": principal,
            "months": months,
            "interest_rate": self.INTEREST_RATE,
            "interest": interest,
            "new_balance": principal + interest
        }

    def credit_interest(self, account_number, months):
        account = self.accounts.get(account_number)
        if not account or months <= 0:
            return False
        preview = self.calculate_interest_preview(account_number, months)
        if not preview:
            return False
        interest_amount = preview["interest"]
        account.balance += interest_amount
        account.total_interest_earned += interest_amount
        account.add_transaction(f"INTEREST ({months}mo)", interest_amount)
        self._save()
        return True
