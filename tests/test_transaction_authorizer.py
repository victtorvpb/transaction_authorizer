import sys
from unittest import TestCase

from transaction_authorizer import transaction_authorizer

from tests.conftest import get_stdout, stub_stdin


class TestTransactionAuthorizer(TestCase):
    stdin = sys.stdin
    maxDiff = None

    def tearDown(self) -> None:
        sys.stdin = self.stdin

    def test_account_not_initialized(self) -> None:
        input_test = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}'  # noqa
        stub_stdin(self, input_test)

        transaction_authorizer()
        output = get_stdout()
        self.assertEqual(
            output,
            str({"account": {}, "violations": ["account-not-initialized"]}),
        )

    def test_integrated_initialize_account(self) -> None:
        input_stdin = (
            '{"account": {"active-card": true, "available-limit": 1000}}'
        )
        stub_stdin(self, input_stdin)
        transaction_authorizer()

        output = get_stdout()
        self.assertEqual(
            output,
            '{"account": {"active-card": true, "available-limit": 1000}, "violations": []}',
        )

    def test_integrated_initialize_with_error(self) -> None:
        input_stdin = (
            '{"account": {"active-card": true, "available-limit": 1000}}\n'
            '{"transaction": {"merchant": "Vivara", "amount": 1250, "time": "2019-02-13T11:00:00.000Z"}}\n'
            '{"transaction": {"merchant": "Samsung", "amount": 2500, "time": "2019-02-13T11:00:01.000Z"}}\n'
            '{"transaction": {"merchant": "Nike", "amount": 200, "time": "2019-02-13T11:01:01.000Z"}}\n'
            '{"transaction": {"merchant": "Nike", "amount": 200, "time": "2019-02-13T11:03:01.000Z"}}\n'
            '{"transaction": {"merchant": "Nike", "amount": 100, "time": "2019-02-13T11:03:01.000Z"}}\n'
            '{"transaction": {"merchant": "Nike", "amount": 100, "time": "2019-02-13T11:03:01.000Z"}}'
        )
        stub_stdin(self, input_stdin)
        transaction_authorizer()

        stdout_output = (
            '{"account": {"active-card": true, "available-limit": 1000}, "violations": []}\n'
            '{"account": {"active-card": true, "available-limit": 1000}, "violations": ["insufficient-limit"]}\n'
            '{"account": {"active-card": true, "available-limit": 1000}, "violations": ["insufficient-limit"]}\n'
            '{"account": {"active-card": true, "available-limit": 800}, "violations": []}\n'
            '{"account": {"active-card": true, "available-limit": 800}, "violations": ["double-transaction"]}\n'
            '{"account": {"active-card": true, "available-limit": 700}, "violations": []}\n'
            '{"account": {"active-card": true, "available-limit": 700}, "violations": ["high-frequency-small-interval", "double-transaction"]}'
        )

        output = get_stdout()
        self.assertEqual(
            output,
            stdout_output,
        )
