from typing import List
from .normalizer_adapters.base import BaseNormalizer


class Normalizer:

    def __init__(self, normalizer_adapters: List[BaseNormalizer]):
        self.normalizer_adapters = normalizer_adapters

    def normalize(self, key, value):
        for normalizer_adapter in self.normalizer_adapters:
            if key in normalizer_adapter.key_matchers:
                return self._normalize(value, normalizer_adapter)

    def _normalize(self, value, normalizer_adapter):
        if isinstance(value, list):
            _res = [normalizer_adapter.normalize(v) for v in value]
            return [r for r in _res if r]

        return normalizer_adapter.normalize(value)
