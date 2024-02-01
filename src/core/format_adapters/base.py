from abc import ABC, abstractmethod


class BaseParseableObject(ABC):

    def __init__(self, payload: str):
        self.payload = payload

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def is_valid_format(self) -> bool:
        pass
