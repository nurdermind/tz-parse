import re
from .base import BaseNormalizer

# Регулярные выражения для поиска интервалов
year_regex = r"\b(?:\d+|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять)\s+(?:год|года|лет)\b"
month_regex = r"\b(?:\d+|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять|полгода)\s+месяц(?:а|ев)?\b"
week_regex = r"\b(?:\d+|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять)\s+недел(?:я|и|ь)\b"
day_regex = r"\b(?:\d+|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять)\s+д(?:ень|ня|ней)\b"

num_dict = {
    "один": 1, "одна": 1, "полгода": 6, "два": 2, "две": 2,
    "три": 3, "четыре": 4, "пять": 5, "шесть": 6,
    "семь": 7, "восемь": 8, "девять": 9, "десять": 10
}


class PeriodNormalizer(BaseNormalizer):
    key_matchers = ['СрокОплаты']

    @classmethod
    def normalize(cls, value: str):
        return cls._convert_time_periods(value)

    @classmethod
    def check_format(cls, value: str):
        return any([
            cls._find_matches(year_regex, value),
            cls._find_matches(month_regex, value),
            cls._find_matches(week_regex, value),
            cls._find_matches(day_regex, value),
        ])

    @staticmethod
    def _find_matches(regex, text):
        """Ищет все совпадения в тексте с использованием регулярного выражения."""
        return re.findall(regex, text)

    @classmethod
    def _convert_and_sum(cls, regex, text, multiplier):
        """Конвертирует найденные совпадения в числа и суммирует их."""
        years, months, weeks, days = 0, 0, 0, 0
        for match in cls._find_matches(regex, text):
            num = match.split()[0]
            value = num_dict.get(num, None)
            if value is None:
                value = int(num)
            if multiplier == "year":
                years += value
            elif multiplier == "month":
                months += value
            elif multiplier == "week":
                weeks += value
            elif multiplier == "day":
                days += value
        return years, months, weeks, days

    @classmethod
    def _convert_time_periods(cls, text):

        # Поиск и преобразование для каждого интервала
        y, m, w, d = cls._convert_and_sum(year_regex, text, "year")
        y1, m1, w1, d1 = cls._convert_and_sum(month_regex, text, "month")
        y2, m2, w2, d2 = cls._convert_and_sum(week_regex, text, "week")
        y3, m3, w3, d3 = cls._convert_and_sum(day_regex, text, "day")

        # Суммирование всех найденных интервалов
        total_years = y + y1 + y2 + y3
        total_months = m + m1 + m2 + m3
        total_weeks = w + w1 + w2 + w3
        total_days = d + d1 + d2 + d3

        return f"{total_years}_{total_months}_{total_weeks}_{total_days}"
