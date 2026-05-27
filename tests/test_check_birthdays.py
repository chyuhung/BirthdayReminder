import datetime
import importlib
import sys
import types
import unittest


class FakeLunarDate:
    def __init__(self, year, month, day):
        self.lunar_year = year
        self.lunar_month = month
        self.lunar_day = day

    def __sub__(self, other):
        left = datetime.date(self.lunar_year, self.lunar_month, self.lunar_day)
        right = datetime.date(other.lunar_year, other.lunar_month, other.lunar_day)
        return (left - right).days


class FakeZhDate:
    @staticmethod
    def from_datetime(value):
        return FakeLunarDate(value.year, value.month, value.day)

    def __new__(cls, year, month, day):
        return FakeLunarDate(year, month, day)


def load_module():
    fake_module = types.ModuleType('zhdate')
    fake_module.ZhDate = FakeZhDate
    sys.modules['zhdate'] = fake_module
    sys.modules.pop('scripts.check_birthdays', None)
    return importlib.import_module('scripts.check_birthdays')


class BirthdayClassificationTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_solar_today_tomorrow_and_advance_boundaries(self):
        today = datetime.date(2026, 12, 30)
        today_lunar = FakeLunarDate(2026, 12, 30)
        birthdays = [
            {'name': 'Today Solar', 'birthday': '2026-12-30', 'lunar': False},
            {'name': 'Tomorrow Solar', 'birthday': '2026-12-31', 'lunar': False},
            {'name': 'Advance Solar', 'birthday': '2027-01-02', 'lunar': False},
        ]

        advance, today_names, tomorrow = self.module._classify_birthdays(
            today,
            today_lunar,
            birthdays,
            reminder_days=3,
        )

        self.assertEqual(advance, ['Advance Solar'])
        self.assertEqual(today_names, ['Today Solar'])
        self.assertEqual(tomorrow, ['Tomorrow Solar'])

    def test_lunar_rolls_over_to_next_year(self):
        today = datetime.date(2026, 12, 31)
        today_lunar = FakeLunarDate(2026, 12, 31)
        birthdays = [
            {'name': 'Lunar Today', 'birthday': '2026-12-31', 'lunar': True},
            {'name': 'Lunar Tomorrow', 'birthday': '2026-01-01', 'lunar': True},
            {'name': 'Lunar Advance', 'birthday': '2026-01-02', 'lunar': True},
        ]

        advance, today_names, tomorrow = self.module._classify_birthdays(
            today,
            today_lunar,
            birthdays,
            reminder_days=2,
        )

        self.assertEqual(advance, ['Lunar Advance'])
        self.assertEqual(today_names, ['Lunar Today'])
        self.assertEqual(tomorrow, ['Lunar Tomorrow'])

    def test_invalid_birthday_entry_raises(self):
        today = datetime.date(2026, 12, 30)
        today_lunar = FakeLunarDate(2026, 12, 30)

        with self.assertRaises(ValueError):
            self.module._classify_birthdays(
                today,
                today_lunar,
                [{'name': 'Missing birthday'}],
                reminder_days=1,
            )


if __name__ == '__main__':
    unittest.main()
