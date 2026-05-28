"""
Unit tests for Account and AccountManager
"""

import pytest
import os
import tempfile
from bank.account import Account, AccountManager


@pytest.fixture
def manager():
    """Create an AccountManager with a fresh temp storage file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        path = f.name
    
    mgr = AccountManager()
    mgr.storage.DATA_FILE = path
    mgr.accounts = {}
    
    yield mgr
    
    if os.path.exists(path):
        os.unlink(path)


class TestAccountCreation:
    def test_create_account(self, manager):
        acc = manager.create_account("Alice", 1000.0, "1234")
        assert acc.account_number is not None
        assert len(acc.account_number) == 6
        assert acc.name == "Alice"
        assert acc.balance == 1000.0
        assert acc.pin == "1234"
        assert len(acc.transactions) == 1
        assert acc.transactions[0]["type"] == "OPENING"

    def test_create_account_zero_balance(self, manager):
        acc = manager.create_account("Bob", 0.0, "5678")
        assert acc.balance == 0.0
        assert len(acc.transactions) == 0

    def test_unique_account_numbers(self, manager):
        acc1 = manager.create_account("User1", 100, "1111")
        acc2 = manager.create_account("User2", 200, "2222")
        assert acc1.account_number != acc2.account_number

    def test_get_account(self, manager):
        acc = manager.create_account("Charlie", 500, "9999")
        fetched = manager.get_account(acc.account_number)
        assert fetched is not None
        assert fetched.name == "Charlie"

    def test_get_nonexistent_account(self, manager):
        assert manager.get_account("000000") is None


class TestDeposit:
    def test_deposit_success(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.deposit(acc.account_number, 500)
        assert result is True
        assert acc.balance == 1500
        assert len(acc.transactions) == 2
        assert acc.transactions[-1]["type"] == "DEPOSIT"

    def test_deposit_zero_amount(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.deposit(acc.account_number, 0)
        assert result is False
        assert acc.balance == 1000

    def test_deposit_negative_amount(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.deposit(acc.account_number, -100)
        assert result is False

    def test_deposit_nonexistent_account(self, manager):
        result = manager.deposit("000000", 100)
        assert result is False


class TestWithdraw:
    def test_withdraw_success(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.withdraw(acc.account_number, 300)
        assert result is True
        assert acc.balance == 700
        assert acc.transactions[-1]["type"] == "WITHDRAW"

    def test_withdraw_insufficient_balance(self, manager):
        acc = manager.create_account("Alice", 100, "1234")
        result = manager.withdraw(acc.account_number, 200)
        assert result is False
        assert acc.balance == 100

    def test_withdraw_zero_amount(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.withdraw(acc.account_number, 0)
        assert result is False


class TestTransfer:
    def test_transfer_success(self, manager):
        acc1 = manager.create_account("Alice", 1000, "1234")
        acc2 = manager.create_account("Bob", 500, "5678")
        result = manager.transfer(acc1.account_number, acc2.account_number, 300)
        assert result is True
        assert acc1.balance == 700
        assert acc2.balance == 800
        assert acc1.transactions[-1]["type"].startswith("TRANSFER TO")
        assert acc2.transactions[-1]["type"].startswith("TRANSFER FROM")

    def test_transfer_same_account(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.transfer(acc.account_number, acc.account_number, 100)
        assert result is False

    def test_transfer_insufficient_balance(self, manager):
        acc1 = manager.create_account("Alice", 100, "1234")
        acc2 = manager.create_account("Bob", 500, "5678")
        result = manager.transfer(acc1.account_number, acc2.account_number, 200)
        assert result is False

    def test_transfer_nonexistent_account(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.transfer(acc.account_number, "000000", 100)
        assert result is False


class TestInterest:
    def test_interest_preview(self, manager):
        acc = manager.create_account("Alice", 1200, "1234")
        preview = manager.calculate_interest_preview(acc.account_number, 12)
        assert preview is not None
        assert preview["principal"] == 1200
        assert preview["months"] == 12
        assert preview["interest"] == 48.0
        assert preview["new_balance"] == 1248.0

    def test_credit_interest(self, manager):
        acc = manager.create_account("Alice", 1200, "1234")
        result = manager.credit_interest(acc.account_number, 12)
        assert result is True
        assert acc.balance == 1248.0
        assert acc.total_interest_earned == 48.0
        assert acc.transactions[-1]["type"] == "INTEREST (12mo)"

    def test_interest_zero_months(self, manager):
        acc = manager.create_account("Alice", 1000, "1234")
        result = manager.credit_interest(acc.account_number, 0)
        assert result is False

    def test_interest_nonexistent_account(self, manager):
        result = manager.credit_interest("000000", 12)
        assert result is False
