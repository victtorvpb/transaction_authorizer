import sys
from unittest import TestCase

from account import Account


class TestAccount(TestCase):
    def test_validate_empty_transaction(self):
        account = Account(active_card=True, available_limit=0)

        self.assertEqual(account.transactions(), [])

    def test_output_in_initilize_class(self):
        Account(active_card=True, available_limit=0)
        message = '{"account": {"active-card": true, "available-limit": 0}, "violations": []}'

        stdout_output = self.get_stdout(message)
        self.assertEqual(stdout_output, message)

    def test_output_fail_in_initilize_class(self):
        Account(active_card=True, available_limit=0)
        message = '{"teste": {"active-card": true, "available-limit": 0}, "violations": []}'

        stdout_output = self.get_stdout(message)
        self.assertNotEqual(stdout_output, message)

    def get_stdout(self, message):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        return output
