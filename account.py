import json
from typing import List


class Account(object):
    def __init__(self, active_card: bool, available_limit: int) -> None:
        self._active_card = active_card
        self._available_limit = available_limit
        self._success_transactions = []
        self._error_transactions = []

        self.print_account_details()

    def transactions(self):
        return list(
            set().union(self._success_transactions, self._error_transactions)
        )

    def print_account_details(self):
        print(json.dumps(self.account_details()))

    def print_account_alread_initialized(self, violations: List = []):
        formated_msg = self.account_details()
        formated_msg["violations"] = ["account-already-initialized"]

        print(json.dumps(formated_msg))

    def account_details(self):
        return {
            "account": {
                "active-card": self._active_card,
                "available-limit": self._available_limit,
            },
            "violations": [],
        }

    def add_transaction(self, transaction):
        self._success_transactions = transaction
