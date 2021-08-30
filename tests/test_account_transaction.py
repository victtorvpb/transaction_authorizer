import contextlib
from datetime import datetime
from io import StringIO
from unittest import TestCase

from account import Account


class TestAccountTransaction(TestCase):
    def setUp(self) -> None:
        self.account = Account(active_card=True, available_limit=1000)

    def test_format_transaction(self) -> None:
        transaction_input = {
            "merchant": "Burger King",
            "amount": 20,
            "time": "2019-02-13T10:00:00.000Z",
        }

        transaction_formated = self.account._format_transaction(
            transaction_input
        )

        str_time_transaction_formated = datetime.strftime(
            transaction_formated["time"], "%Y-%m-%dT%H:%M:%S.000Z"
        )

        self.assertEqual(
            transaction_input["merchant"], transaction_formated["merchant"]
        )
        self.assertEqual(
            transaction_input["amount"], transaction_formated["amount"]
        )
        self.assertEqual(type(transaction_formated["time"]), datetime)

        self.assertEqual(
            str_time_transaction_formated, transaction_input["time"]
        )

    def test_check_add_transaction_active_card_is_true(self) -> None:
        account = Account(active_card=False, available_limit=1)

        self.assertEqual(
            account._check_add_transaction_not_active_card(), True
        )

    def test_check_add_transaction_active_card_is_false(self) -> None:
        account = Account(active_card=True, available_limit=1)

        self.assertEqual(
            account._check_add_transaction_not_active_card(), False
        )

    def test_check_transaction_available_limit_is_true(self) -> None:
        transaction_input = {
            "merchant": "Burger King",
            "amount": 20,
            "time": "2019-02-13T10:00:00.000Z",
        }

        account = Account(active_card=False, available_limit=1)

        self.assertEqual(
            account._check_transaction_available_limit(transaction_input),
            True,
        )

    def test_check_transaction_available_limit_is_false(self) -> None:

        transaction_input = {
            "merchant": "Burger King",
            "amount": 20,
            "time": "2019-02-13T10:00:00.000Z",
        }
        account = Account(active_card=True, available_limit=30)

        self.assertEqual(
            account._check_transaction_available_limit(transaction_input),
            False,
        )

    def test_add_transaction_whitout_violation(self) -> None:
        transactions_input = [
            (
                {
                    "merchant": "Burger King",
                    "amount": 20,
                    "time": "2019-02-13T10:00:00.000Z",
                },
                '{"account": {"active-card": true, "available-limit": 980}, "violations": []}',
            ),
            (
                {
                    "merchant": "Nike",
                    "amount": 60,
                    "time": "2019-02-13T10:03:00.000Z",
                },
                '{"account": {"active-card": true, "available-limit": 920}, "violations": []}',
            ),
        ]
        for transaction, output_message in transactions_input:
            temp_stdout = StringIO()

            with contextlib.redirect_stdout(temp_stdout):
                self.account.add_transaction(transaction)

                output = temp_stdout.getvalue().strip()
                self.assertEqual(output, output_message)

    def test_add_transaction_whitout_violation(self) -> None:
        transactions_input = [
            (
                {
                    "merchant": "Burger King",
                    "amount": 20,
                    "time": "2019-02-13T10:00:00.000Z",
                },
                '{"account": {"active-card": true, "available-limit": 980}, "violations": []}',
            ),
            (
                {
                    "merchant": "Nike",
                    "amount": 60,
                    "time": "2019-02-13T10:03:00.000Z",
                },
                '{"account": {"active-card": true, "available-limit": 920}, "violations": []}',
            ),
        ]
        for transaction, output_message in transactions_input:
            temp_stdout = StringIO()

            with contextlib.redirect_stdout(temp_stdout):
                self.account.add_transaction(transaction)

                output = temp_stdout.getvalue().strip()
                self.assertEqual(output, output_message)

    def test_add_transaction_whit_high_frequency_violation(self) -> None:
        transaction_input = [
            {
                "merchant": "Samsung",
                "amount": 100,
                "time": "2019-02-13T11:00:01.000Z",
            },
            {
                "merchant": "Nike",
                "amount": 150,
                "time": "2019-02-13T11:01:01.000Z",
            },
            {
                "merchant": "Nike",
                "amount": 200,
                "time": "2019-02-13T11:03:01.000Z",
            },
            {
                "merchant": "Nike",
                "amount": 100,
                "time": "2019-02-13T11:03:01.000Z",
            },
        ]

        temp_stdout = StringIO()
        output_message = '{"account": {"active-card": true, "available-limit": 550}, "violations": ["high-frequency-small-interval"]}'  # noqa
        for transaction in transaction_input[:-1]:
            self.account.add_transaction(transaction)

        with contextlib.redirect_stdout(temp_stdout):
            self.account.add_transaction(transaction_input[-1])
            output = temp_stdout.getvalue().strip()
            self.assertEqual(str(output), output_message)

    def test_add_transaction_whit_double_transaction_violation(self) -> None:
        transaction_input = [
            {
                "merchant": "Samsung",
                "amount": 100,
                "time": "2019-02-13T11:00:01.000Z",
            },
            {
                "merchant": "Nike",
                "amount": 200,
                "time": "2019-02-13T11:01:01.000Z",
            },
            {
                "merchant": "Nike",
                "amount": 200,
                "time": "2019-02-13T11:03:01.000Z",
            },
        ]

        temp_stdout = StringIO()
        output_message = '{"account": {"active-card": true, "available-limit": 700}, "violations": ["double-transaction"]}'  # noqa
        for transaction in transaction_input[:-1]:
            self.account.add_transaction(transaction)

        with contextlib.redirect_stdout(temp_stdout):
            self.account.add_transaction(transaction_input[-1])
            output = temp_stdout.getvalue().strip()
            self.assertEqual(str(output), output_message)
