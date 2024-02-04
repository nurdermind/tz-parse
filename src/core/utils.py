from typing import Hashable

from core.format_adapters.formats import TypeFormat


def walk_dict(d, path=None):
    path = path or []
    for key, value in d.items():
        if isinstance(value, dict):
            yield from walk_dict(value, path + [str(key)])
        else:
            yield key, value, path + [str(key)]


def merge_dicts(a: dict, b: dict, path=None):
    path = path or []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def insert_value_into_dict_with_path(d: dict, path: list[Hashable], value):
    assert len(path) > 0, 'path must be non-empty'

    current_dict = d
    while len(path) > 1:
        next_key = path.pop(0)
        if next_key not in current_dict:
            current_dict[next_key] = {}
        current_dict = current_dict[next_key]

    current_dict[path[0]] = value
    return d


def convert_content_type_to_internal_format(content_type: str) -> TypeFormat:
    content_type = content_type.lower()

    mapper_formats = {
        'application/json': TypeFormat.JSON,
        'application/xml': TypeFormat.XML,
        'text/xml': TypeFormat.XML,
    }

    if content_type not in mapper_formats:
        raise ValueError(f'Content type must be one of {", ".join(mapper_formats.keys())}')

    return mapper_formats[content_type]
