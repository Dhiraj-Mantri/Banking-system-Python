"""
Unit tests for LoanManager
"""

import pytest
import os
import tempfile
from bank.loan import LoanManager


@pytest.fixture
def loan_mgr():
    """Create a LoanManager with a fresh temp storage file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        path = f.name
    
    # Create manager and override its storage path
    mgr = LoanManager()
    mgr.storage.DATA_FILE = path
    mgr.loans = {}
    mgr.repayment_history = []
    
    yield mgr
    
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


class TestEMICalculation:
    def test_calculate_emi_basic(self):
        emi = LoanManager.calculate_emi(10000, 0.10, 12)
        assert emi > 0
        assert round(emi, 2) == 879.16

    def test_calculate_emi_zero_principal(self):
        emi = LoanManager.calculate_emi(0, 0.10, 12)
        assert emi == 0.0

    def test_calculate_emi_zero_months(self):
        emi = LoanManager.calculate_emi(10000, 0.10, 0)
        assert emi == 0.0

    def test_calculate_emi_zero_rate(self):
        emi = LoanManager.calculate_emi(12000, 0, 12)
        assert emi == 1000.0


class TestLoanApplication:
    def test_apply_loan(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", 10000, 0.10, 12)
        assert loan is not None
        assert loan["loan_id"].startswith("L")
        assert loan["principal"] == 10000
        assert loan["status"] == "active"
        assert loan["remaining_amount"] > 0
        assert loan["emi"] > 0

    def test_apply_loan_invalid_amount(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", -1000, 0.10, 12)
        assert loan is None

    def test_apply_loan_invalid_months(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", 10000, 0.10, 0)
        assert loan is None


class TestLoanRepayment:
    def test_repay_emi(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", 10000, 0.10, 12)
        emi = loan["emi"]
        result = loan_mgr.repay_emi(loan["loan_id"], emi)
        assert result is not None
        assert result["total_paid"] == emi
        assert result["remaining_amount"] < result["total_payable"]

    def test_repay_full_loan(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", 1000, 0.10, 1)
        total = loan["total_payable"]
        result = loan_mgr.repay_emi(loan["loan_id"], total)
        assert result["status"] == "paid"
        assert result["remaining_amount"] == 0

    def test_repay_nonexistent_loan(self, loan_mgr):
        result = loan_mgr.repay_emi("L00000", 100)
        assert result is None

    def test_repay_zero_amount(self, loan_mgr):
        loan = loan_mgr.apply_loan("123456", 10000, 0.10, 12)
        result = loan_mgr.repay_emi(loan["loan_id"], 0)
        assert result is None


class TestLoanQueries:
    def test_get_loans_by_account(self, loan_mgr):
        loan1 = loan_mgr.apply_loan("111111", 5000, 0.10, 12)
        loan2 = loan_mgr.apply_loan("111111", 3000, 0.10, 6)
        loan_mgr.apply_loan("222222", 10000, 0.10, 24)
        
        loans = loan_mgr.get_loans_by_account("111111")
        assert len(loans) == 2

    def test_get_active_loans(self, loan_mgr):
        loan = loan_mgr.apply_loan("111111", 1000, 0.10, 1)
        loan_mgr.repay_emi(loan["loan_id"], loan["total_payable"])
        
        active = loan_mgr.get_active_loans("111111")
        assert len(active) == 0
