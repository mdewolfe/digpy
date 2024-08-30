from typing import Any, NamedTuple

class Result(NamedTuple):
    found: bool
    value: Any = None

def dig(*, keypath: list, source: list|dict) -> Result:
    if not keypath or not source:
        return Result(found=False)

    key = keypath[0]
    try:
        value = source[key]
        if len(keypath) == 1:
            return Result(found=True, value=value)

        if not isinstance(value, (dict,list)):
            return Result(found=False)

        return dig(keypath=keypath[1:], source=value)
    except (KeyError, IndexError, TypeError):
        pass

    return Result(found=False)
