"""
Loan Management System
"""

import random
from datetime import datetime
from .storage import Storage


class LoanManager:
    LOAN_RATE = 0.10  # 10% annual

    def __init__(self):
        self.storage = Storage("data/loans.json")
        self.loans = {}
        self.repayment_history = []
        self._load_loans()

    def _load_loans(self):
        data = self.storage.load()
        if isinstance(data, dict):
            self.loans = data.get("loans", {})
            self.repayment_history = data.get("history", [])
        else:
            self.loans = {}
            self.repayment_history = []

    def _save(self):
        self.storage.save({"loans": self.loans, "history": self.repayment_history})

    def _generate_loan_id(self):
        while True:
            lid = f"L{random.randint(10000, 99999)}"
            if lid not in self.loans:
                return lid

    @staticmethod
    def calculate_emi(principal, annual_rate, months):
        if principal <= 0 or months <= 0:
            return 0.0
        monthly_rate = annual_rate / 12
        if monthly_rate == 0:
            return principal / months
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) /               ((1 + monthly_rate) ** months - 1)
        return round(emi, 2)

    def apply_loan(self, account_number, principal, annual_rate, months):
        if principal <= 0 or months <= 0:
            return None
        loan_id = self._generate_loan_id()
        emi = self.calculate_emi(principal, annual_rate, months)
        total_payable = emi * months
        loan = {
            "loan_id": loan_id,
            "account_number": account_number,
            "principal": principal,
            "annual_rate": annual_rate,
            "months": months,
            "emi": emi,
            "total_payable": total_payable,
            "total_paid": 0.0,
            "remaining_amount": total_payable,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "repayments": []
        }
        self.loans[loan_id] = loan
        self._save()
        return loan

    def get_loan(self, loan_id):
        return self.loans.get(loan_id)

    def get_loans_by_account(self, account_number):
        return [loan for loan in self.loans.values() if loan["account_number"] == account_number]

    def get_active_loans(self, account_number):
        return [loan for loan in self.loans.values() 
                if loan["account_number"] == account_number and loan["status"] == "active"]

    def repay_emi(self, loan_id, amount):
        loan = self.loans.get(loan_id)
        if not loan or loan["status"] != "active" or amount <= 0:
            return None
        repayment = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "amount": amount}
        loan["repayments"].append(repayment)
        loan["total_paid"] += amount
        loan["remaining_amount"] = max(0, loan["remaining_amount"] - amount)
        self.repayment_history.append({
            "date": repayment["date"],
            "loan_id": loan_id,
            "account_number": loan["account_number"],
            "amount": amount,
            "type": "EMI PAYMENT"
        })
        if loan["remaining_amount"] <= 0:
            loan["status"] = "paid"
            loan["remaining_amount"] = 0
        self._save()
        return loan

    def get_repayment_history(self, account_number):
        return [entry for entry in self.repayment_history 
                if entry["account_number"] == account_number]
