import re
from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseNormalizer(ABC):
    key_matchers: List[str] = []

    @classmethod
    @abstractmethod
    def check_format(cls, value: str):
        pass

    @classmethod
    @abstractmethod
    def normalize(cls, value: str):
        pass
