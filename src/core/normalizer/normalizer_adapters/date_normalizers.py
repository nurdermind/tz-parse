import locale
import re
from datetime import datetime
from typing import List, Callable, Optional

from .base import BaseNormalizer


def date_converter_maker(date_format: str, regex: re.Pattern = None) -> Callable:
    def _wrap(date_str: str) -> Optional[str]:
        date_str = date_str.lower()
        if regex and (match := regex.match(date_str)):
            date_str = match.group()
        try:
            return datetime.strptime(date_str, date_format).strftime('%d.%m.%Y')
        except ValueError:
            return

    return _wrap


def human_month_date_converter_maker(date_format: str, regex: re.Pattern = None) -> Callable:
    def _wrap(date_str: str) -> Optional[str]:
        date_converter = date_converter_maker(date_format, regex)
        init_locale = locale.getlocale()
        result = None

        for locale_alias in locale.locale_alias.values():
            try:
                locale.setlocale(locale.LC_TIME, locale_alias)
                if result := date_converter(date_str):
                    break
            except (ValueError, locale.Error):
                pass

        locale.setlocale(locale.LC_TIME, '.'.join(init_locale))
        return result

    return _wrap


class DateNormalizer(BaseNormalizer):
    converters: List[Callable] = [
        human_month_date_converter_maker('%d %B %Y', regex=re.compile(r'\d+\s*[\wА-я]+\s*\d+')),
        human_month_date_converter_maker('%d %B %Y'),
        date_converter_maker('%Y-%m-%d'),
        date_converter_maker('%Y.%m.%d'),
        date_converter_maker('%d.%m.%Y'),
    ]
    key_matchers = ['ДатаДокумента']

    @classmethod
    def check_format(cls, value: str):
        for converter in cls.converters:
            if converter(value):
                return True
        return False

    @classmethod
    def normalize(cls, value: str):
        for converter in cls.converters:
            if result := converter(value):
                return result
        raise ValueError('Normalize error')
