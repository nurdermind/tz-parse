from xml.parsers.expat import ExpatError

from xmltodict import parse

from core.format_adapters.base import BaseParseableObject


class XmlAdapter(BaseParseableObject):

    def get_data(self) -> dict:
        return parse(self.payload)

    def is_valid_format(self) -> bool:
        try:
            parse(self.payload)
            return True
        except ExpatError:
            return False
