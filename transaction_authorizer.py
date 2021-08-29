import sys

from account import Account
from utils import convert_str_to_dict


def transaction_authorizer():
    account = None
    lines = sys.stdin.readlines()
    for line in lines:
        line_converted_in_dict = convert_str_to_dict(line)

        if line_converted_in_dict.get("account") and not account:
            data_line = line_converted_in_dict["account"]
            account = Account(
                active_card=data_line["active-card"],
                available_limit=data_line["available-limit"],
            )
        elif line_converted_in_dict.get("account") and account:
            account.print_account_alread_initialized()
        elif line_converted_in_dict.get("transaction"):
            if not account:
                print(
                    {"account": {}, "violations": ["account-not-initialized"]}
                )
            else:
                pass


if __name__ == "__main__":
    transaction_authorizer()
