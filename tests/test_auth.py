"""
Unit tests for Authentication
"""

import pytest
import os
import tempfile
from bank.auth import AuthManager
from bank.account import AccountManager


@pytest.fixture
def auth_setup():
    """Create fresh auth and manager with temp storage."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        path = f.name
    
    mgr = AccountManager()
    mgr.storage.DATA_FILE = path
    mgr.accounts = {}
    
    auth = AuthManager()
    
    yield auth, mgr
    
    if os.path.exists(path):
        os.unlink(path)


class TestAuthentication:
    def test_valid_login(self, auth_setup):
        auth, mgr = auth_setup
        acc = mgr.create_account("Alice", 1000, "1234")
        result = auth.authenticate(acc.account_number, "1234", mgr)
        assert result is not None
        assert result.name == "Alice"

    def test_invalid_pin(self, auth_setup):
        auth, mgr = auth_setup
        acc = mgr.create_account("Alice", 1000, "1234")
        result = auth.authenticate(acc.account_number, "9999", mgr)
        assert result is None

    def test_nonexistent_account(self, auth_setup):
        auth, mgr = auth_setup
        result = auth.authenticate("000000", "1234", mgr)
        assert result is None
