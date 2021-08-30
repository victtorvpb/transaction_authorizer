import contextlib
from io import StringIO
from unittest import TestCase

from account import Account

from tests.conftest import get_stdout


class TestAccount(TestCase):
    def test_validate_empty_transaction(self) -> None:
        account = Account(active_card=True, available_limit=0)

        self.assertEqual(account._Account__transactions, [])

    def test_output_in_initilize_class(self) -> None:
        Account(active_card=True, available_limit=0)
        message = '{"account": {"active-card": true, "available-limit": 0}, "violations": []}'  # noqa

        stdout_output = get_stdout()
        self.assertEqual(stdout_output, message)

    def test_output_fail_in_initilize_class(self) -> None:
        Account(active_card=True, available_limit=0)
        message = '{"teste": {"active-card": true, "available-limit": 0}, "violations": []}'  # noqa

        stdout_output = get_stdout()
        self.assertNotEqual(stdout_output, message)

    def test_print_account_alread_initialized(self) -> None:
        account = Account(active_card=True, available_limit=0)
        message = '{"account": {"active-card": true, "available-limit": 0}, "violations": ["account-already-initialized"]}'  # noqa

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):

            account.print_account_alread_initialized()

        output = temp_stdout.getvalue().strip()

        self.assertEqual(output, message)

    def test_print_account_alread_initialized_fail(self) -> None:
        account = Account(active_card=True, available_limit=0)

        message = '{"teste": {"active-card": true, "available-limit": 0}, "violations": []}'  # noqa
        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):

            account.print_account_alread_initialized()

        output = temp_stdout.getvalue().strip()
        self.assertNotEqual(output, message)
