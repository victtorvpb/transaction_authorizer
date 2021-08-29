import sys
from io import StringIO


def get_stdout():
    if not hasattr(sys.stdout, "getvalue"):
        print("need to run in buffered mode")

    output = sys.stdout.getvalue().strip()
    return output


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = StringIO(inputs)
