from typing import List

from .format_adapters import format_adapters_classes
from .normalizer import normalizer
from .utils import merge_dicts, walk_dict, insert_value_into_dict_with_path


class Parser:

    def __init__(self, payloads: List[str]):
        self._data = {}
        for payload in payloads:
            adapter = self._get_format_adapter(payload)
            self._data = merge_dicts(self._data, adapter.get_data())

    def parse(self) -> dict:
        for key, value, path in walk_dict(self._data):
            if normalized_value := normalizer.normalize(key, value):
                self._data = insert_value_into_dict_with_path(self._data, path, normalized_value)
        return self._data

    @staticmethod
    def _get_format_adapter(payload: str):
        for adapter_class in format_adapters_classes:
            adapter = adapter_class(payload)
            if adapter.is_valid_format():
                return adapter
        else:
            raise ValueError("Invalid format for parsing")
