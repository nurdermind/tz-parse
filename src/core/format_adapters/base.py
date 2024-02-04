from abc import ABC, abstractmethod
from typing import List

from core.format_adapters.formats import TypeFormat


class BaseParseableObject(ABC):
    comparable_formats: List[TypeFormat] = []

    def __init__(self, payload: str):
        self.payload = payload

    @classmethod
    def check_comparable_format(cls, type_format: str) -> bool:
        return type_format in cls.comparable_formats

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def is_valid_format(self) -> bool:
        pass

