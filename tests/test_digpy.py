import json
from typing import cast

import pytest

from digpy.dig import Result, dig


def test_empty_path():
    result: Result = dig(keypath=[], source={"foo": 1})
    assert result.found is False
    assert result.value is None


def test_empty_path_default_value():
    result: Result = dig(keypath=[], source={"foo": 1}, default_value=42)
    assert result.found is False
    assert result.value == 42


def test_keypath_is_none():
    result: Result = dig(keypath=cast(list, None), source={"foo": 1})
    assert result.found is False
    assert result.value is None


def test_source_empty_dict():
    result: Result = dig(keypath=["foo"], source={})
    assert result.found is False
    assert result.value is None


def test_source_empty_dict_default_value():
    result: Result = dig(keypath=["foo"], source={}, default_value="fortytwo")
    assert result.found is False
    assert result.value == "fortytwo"


def test_source_empty_list():
    result: Result = dig(keypath=["foo"], source=[])
    assert result.found is False
    assert result.value is None


def test_source_is_none():
    result: Result = dig(keypath=["foo"], source=cast(dict, None))
    assert result.found is False
    assert result.value is None


def test_source_is_none_default_value():
    result: Result = dig(
        keypath=["foo"], source=cast(dict, None), default_value="forty and two"
    )
    assert result.found is False
    assert result.value == "forty and two"


def test_source_is_string():
    # given
    source = "helloworld"

    # when
    result: Result = dig(keypath=["hello", "worls"], source=cast(dict, source))

    # then
    assert result.found is False
    assert result.value is None


def test_source_is_arbitrary_object():
    # given
    class Foo:
        def __init__(self, prop_1):
            self.hello = prop_1

    source = Foo(prop_1="world")

    # when
    result: Result = dig(keypath=["hello"], source=cast(dict, source))

    # then
    assert result.found is False
    assert result.value is None


def test_source_is_number():
    # given
    source = 42

    # when
    result: Result = dig(keypath=["hello", "worls"], source=cast(dict, source))

    # then
    assert result.found is False
    assert result.value is None


def test_simple_dict():
    # given
    source = {"some_key": 42, "other_key": "hello, world!"}

    # when
    result: Result = dig(keypath=["some_key"], source=source)

    # then
    assert result.found is True
    assert result.value == 42


def test_simple_list():
    # given
    source = [9, 8, 7]

    # when
    result: Result = dig(keypath=[1], source=source)

    # then
    assert result.value == 8
    assert result.found is True


def test_simple_list_negative_index():
    # given
    source = [9, 8, 7]

    # when
    result: Result = dig(keypath=[-1], source=source)

    # then
    assert result.value == 7
    assert result.found is True


def test_key_not_resent():
    # given
    source = {"some_key": 42, "other_key": "hello, world!"}

    # when
    result = dig(keypath=["key_three"], source=source)

    # then
    assert result.value is None
    assert result.found is False


def test_key_not_resent_default_value():
    # given
    source = {"some_key": 42, "other_key": "hello, world!"}

    # when
    result = dig(keypath=["key_three"], source=source, default_value=42)

    # then
    assert result.found is False
    assert result.value == 42


def test_index_out_of_range():
    # given
    source = [9, 8, 7]

    # when
    result = dig(keypath=[3], source=source)

    # then
    assert result.value is None
    assert result.found is False


def test_index_out_of_range_default_value():
    # given
    source = [9, 8, 7]

    # when
    result = dig(keypath=[3], source=source, default_value=42)

    # then
    assert result.found is False
    assert result.value == 42


def test_valid_none_is_found():
    # given
    source = {"some_key": None, "other_key": "hello, world!"}

    # when
    result: Result = dig(keypath=["some_key"], source=source)

    # then
    assert result.value is None
    assert result.found is True


@pytest.fixture
def sample_json():
    with open("tests/fixtures/sample.json") as fp:
        sample = json.load(fp)

    return sample


def test_complex_json_array(sample_json):
    # given
    keypath = [2, "commit", "author", "date"]

    # when
    result: Result = dig(keypath=keypath, source=sample_json)

    # then
    assert result.found is True
    assert result.value == "2024-08-21T23:17:54Z"


def test_complex_json_array_key_not_found(sample_json):
    # given
    keypath = [2, "commit", "foo", "date"]

    # when
    result: Result = dig(keypath=keypath, source=sample_json)

    # then
    assert result.found is False
    assert result.value is None


def test_complex_json_array_key_not_found_default_value(sample_json):
    # given
    keypath = [2, "commit", "foo", "date"]

    # when
    result: Result = dig(keypath=keypath, source=sample_json, default_value=42)

    # then
    assert result.found is False
    assert result.value == 42
