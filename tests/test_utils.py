from typing import Dict
from unittest import TestCase

from utils import convert_str_to_dictstr_text


class TestUtils(TestCase):
    def test_convert_json_to_dict_type(self):
        input_test = '{"account": {"active-card": true, "available-limit": 100}}'
        result = convert_str_to_dictstr_text(input_test)
        self.assertEqual(type(result), dict)

    def test_convert_json_to_dict(self):
        input_test = [
            ('{"test": 1}', "test", 1),
            ('{"test2": "text"}', "test2", "text"),
            ('{"test3": true}', "test3", True),
            ('{"test3": true}', "test4", None),
        ]

        for dict_text, key_test, value_test in input_test:
            with self.subTest():
                result = convert_str_to_dictstr_text(dict_text)
                self.assertEqual(result.get(key_test), value_test)
