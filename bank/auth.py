"""
Simple Authentication Manager
"""


class AuthManager:
    def authenticate(self, account_number, pin, account_manager):
        account = account_manager.get_account(account_number)
        if account and account.pin == pin:
            return account
        return None
