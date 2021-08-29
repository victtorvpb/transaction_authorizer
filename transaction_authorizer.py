import json
import sys

from utils import convert_str_to_dict


def transaction_authorizer():
    lines = sys.stdin.readlines()
    for line in lines:
        if not account and line.get("account"):
            account = convert_str_to_dict(line)
            account["violations"] = []
            sys.stdout.write(str(account))


if __name__ == "__main__":
    transaction_authorizer()
