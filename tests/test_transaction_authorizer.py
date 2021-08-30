import sys
from unittest import TestCase

from transaction_authorizer import transaction_authorizer

from tests.conftest import get_stdout, stub_stdin


class TestTransactionAuthorizer(TestCase):
    stdin = sys.stdin

    def tearDown(self) -> None:
        sys.stdin = self.stdin

    def test_account_not_initialized(self):
        input_test = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}'  # noqa
        stub_stdin(self, input_test)

        transaction_authorizer()
        output = get_stdout()
        self.assertEqual(
            output,
            str({"account": {}, "violations": ["account-not-initialized"]}),
        )
