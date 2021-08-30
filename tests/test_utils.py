from datetime import datetime
from unittest import TestCase

from utils import convert_str_to_datetime, convert_str_to_dict


class TestUtils(TestCase):
    def test_convert_json_to_dict_type(self):
        input_test = (
            '{"account": {"active-card": true, "available-limit": 100}}'
        )
        result = convert_str_to_dict(input_test)
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
                result = convert_str_to_dict(dict_text)
                self.assertEqual(result.get(key_test), value_test)

    def test_convert_datetime_to_str(self):

        datetime_str = "2020-12-01T11:07:00.000Z"

        converted_str = convert_str_to_datetime(datetime_str)

        self.assertEqual(datetime, type(converted_str))
        self.assertEqual(converted_str.year, 2020)
        self.assertEqual(converted_str.month, 12)
        self.assertEqual(converted_str.hour, 11)
        self.assertEqual(converted_str.minute, 7)
        self.assertEqual(converted_str.day, 1)
