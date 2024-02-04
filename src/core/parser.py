import time
from typing import List

from .format_adapters import format_adapters_classes
from .format_adapters.formats import TypeFormat
from .normalizer import normalizer
from .utils import merge_dicts, walk_dict, insert_value_into_dict_with_path


class Parser:

    def __init__(self, payloads: List[str], type_format: TypeFormat):
        self._data = {}
        self.type_format = type_format
        for payload in payloads:
            adapter = self._get_format_adapter(payload)
            self._data = merge_dicts(self._data, adapter.get_data())

    def parse(self) -> dict:
        for key, value, path in walk_dict(self._data):
            print('Emulating throttle (2s)...')
            time.sleep(2)
            if normalized_value := normalizer.normalize(key, value):
                self._data = insert_value_into_dict_with_path(self._data, path, normalized_value)
        return self._data

    def _get_format_adapter(self, payload: str):
        comparable_adapters = [
            adapter_class
            for adapter_class in format_adapters_classes
            if adapter_class.check_comparable_format(self.type_format)
        ]
        if not comparable_adapters:
            raise ValueError(f"No adapter found for format type {self.type_format}")
        for adapter_class in comparable_adapters:
            adapter = adapter_class(payload)
            if adapter.is_valid_format():
                return adapter
        else:
            raise ValueError("Invalid format for parsing")
