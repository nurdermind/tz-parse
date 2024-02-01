import json

from core.format_adapters.base import BaseParseableObject


class JsonAdapter(BaseParseableObject):

    def get_data(self) -> dict:
        return json.loads(self.payload)

    def is_valid_format(self) -> bool:
        try:
            json.loads(self.payload)
            return True
        except json.JSONDecodeError:
            return False
