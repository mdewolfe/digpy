# digpy

## Preamble and Rant

> [!CAUTION]
> You probably do not need this micro package. See why [here](https://bvisness.me/microlibraries) and/or [here](https://youtu.be/IVmIEtwsaYk).


## Motivations

This little library was designed for a specific use case when parsing JSON data.
We were constantly doing trying to get values nested multiple layers deep in a JSON
object. We were constantly wrapping code in `try-except` blocks or chaining `dict.get`
calls. Coming from Ruby on Rails background, [`Hash.dig` function](https://apidock.com/ruby/v2_5_5/Hash/dig)
was immensely convenient to avoid the clutter of exception handling and/or sequentially
calling `dict.get`. Another reason, after playing around with Go and Rust, I came
to appreciate [errors as values](https://www.inngest.com/blog/python-errors-as-values).
In this case, and my use case, one of `KeyError`, `ÌndexError`, or `TypeError`, are
reasonable errors to encounter when handling (mostly) arbitrary JSON data.

> [!NOTE]
> True, errors are not really returned, but potential common errors are handled.


Consider the follwing object:

```json
{
  "customer": {
    "purchase": {
      "subscriptions": [
        {
          "name": "Subsciption the First",
          "cadence": "month",
          "price": 42,
          "status": "paid"
        },
        {
          "name": "Subsciption the Second",
          "cadence": "year",
          "price": 420,
          "status": "expired"
        },
      ]
    }
  }
}
```

> [!NOTE]
> The objects we were dealing with were more complex.

If we want the list if subscriptions, we had two options:

1. Handle exceptions that would be ignored anyways:
    ```py
    try:
        return  json["customer"]["purchase"]["subscriptions"]
    except KeyError:
        return None
    ```
    But I do not particularly like having exceptions all over the place, especially
    with my use case. This was cumbersome.

2. Chain `dict.get`
    ```py
    return json.get("customer", {}).get("purchase", {}).get("subscriptions", [])
    ```
    Similar to the staregy above, with the nesting and repetition, this would clutter
    the code needlessly when all I want to know if a value is at the end of that
    keypath.

Constant repetition of these patterns was tedious, and we had multiple projects that
followed the same pattern, increasing the tedium. Repetitive code is the bane to the
existence of all programmers.


## Installation

### Pre-Requisites

A compatible Python versions: 3.9, 3.10, 3.11, 3.12

TODO


## Usage

Pass in a path to the nested value and provide the source, and an optional default
value: (defaults to `None`:)

```py
# TODO: simplify the import
from digpy.dig import dig

json = fetch_json_example_above()
result = dig(keypath=["customer", "purchase", "subscriptions"], default_value=[])
if result.found:
    handle_found_result(result.value)
else:
    handle_not_fount(result.value)
```

One assumption that is made is the expected value is nested at the end of the keypath.

### `Result` Object

```py
class Result(NamedTuple):
    found: bool
    value: Optional[Any] = None
```

The result object has two properties:
- `found`: `true` if a value was found nested at the end of the keypath, `false` otherwise
- `value`: Will be the object found nested at the end of the `keypath`. Otherwise,
  it will contain the default value.
