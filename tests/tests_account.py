from unittest import TestCase

from account import Account

from tests.conftest import get_stdout


class TestAccount(TestCase):
    def test_validate_empty_transaction(self):
        account = Account(active_card=True, available_limit=0)

        self.assertEqual(account._Account__transactions, [])

    def test_output_in_initilize_class(self):
        Account(active_card=True, available_limit=0)
        message = '{"account": {"active-card": true, "available-limit": 0}, "violations": []}'  # noqa

        stdout_output = get_stdout()
        self.assertEqual(stdout_output, message)

    def test_output_fail_in_initilize_class(self):
        Account(active_card=True, available_limit=0)
        message = '{"teste": {"active-card": true, "available-limit": 0}, "violations": []}'  # noqa

        stdout_output = get_stdout()
        self.assertNotEqual(stdout_output, message)
