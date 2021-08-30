import json
from copy import deepcopy
from datetime import date, datetime, timedelta
from typing import Dict, List

from utils import convert_str_to_datetime


class Account(object):
    def __init__(self, active_card: bool, available_limit: int) -> None:
        self._active_card = active_card
        self.__limit = available_limit
        self.__available_limit = available_limit
        self.__transactions = []

        self.print_account_details()

    def print_account_details(self) -> None:
        print(json.dumps(self.account_details()))

    def print_account_alread_initialized(self) -> None:
        self.print_account_violations(["account-already-initialized"])

    def print_account_violations(self, violations: List = []) -> None:
        formated_msg = self.account_details()
        formated_msg["violations"] = violations

        print(json.dumps(formated_msg))

    def account_details(self) -> Dict:
        return {
            "account": {
                "active-card": self._active_card,
                "available-limit": self.__available_limit,
            },
            "violations": [],
        }

    def add_transaction(self, transaction: Dict) -> None:

        transaction_copy = deepcopy(transaction)

        transaction_copy = self._format_transaction(transaction)
        violations = self._check_transaction_violation(transaction_copy)

        if violations:
            self.print_account_violations(violations)
            return None

        self.__available_limit -= transaction_copy["amount"]

        self.__transactions.append(transaction_copy)
        self.print_account_details()

    def _format_transaction(self, transaction: Dict) -> Dict:
        transaction_copy = deepcopy(transaction)

        transaction_copy["time"] = convert_str_to_datetime(
            transaction_copy["time"]
        )
        return transaction_copy

    def _check_transaction_violation(self, transaction: Dict) -> List:
        violations = []
        transaction_copy = deepcopy(transaction)

        if self._check_add_transaction_not_active_card():
            violations.append("card-not-active")

        if self._check_transaction_available_limit(transaction_copy):
            violations.append("insufficient-limit")

        if self._check_high_frequency_small_interval(transaction_copy):
            violations.append("high-frequency-small-interval")

        if self._check_double_transaction(transaction_copy):
            violations.append("double-transaction")

        return violations

    def _check_add_transaction_not_active_card(self) -> bool:
        if not self._active_card:
            return True

        return False

    def _check_transaction_available_limit(self, transaction) -> bool:
        if self.__available_limit < transaction["amount"]:
            return True

        return False

    def _check_high_frequency_small_interval(self, transaction) -> bool:
        datetime_to_check = transaction["time"] - timedelta(minutes=2)
        transaction_count = 0

        for i in reversed(self.__transactions):
            if (
                i["merchant"] == transaction["merchant"]
                and i["time"] >= datetime_to_check
            ):
                transaction_count += 1

            if transaction_count == 2:
                return True

        return False

    def _check_double_transaction(self, transaction) -> bool:
        datetime_to_check = transaction["time"] - timedelta(minutes=2)

        for i in reversed(self.__transactions):
            if (
                i["merchant"] == transaction["merchant"]
                and i["amount"] == transaction["amount"]
                and i["time"] >= datetime_to_check
            ):
                return True

        return False
