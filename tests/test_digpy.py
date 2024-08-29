import json
from typing import cast
import pytest
from digpy.dig import dig, Result


def test_empty_path():
    result: Result = dig(keypath=[], source={"foo":1})
    assert result.found is False
    assert result.value is None


def test_keypath_is_none():
    result: Result = dig(keypath=cast(list, None), source={"foo":1})
    assert result.found is False
    assert result.value is None


def test_source_empty_dict():
    result: Result = dig(keypath=["foo"], source={})
    assert result.found is False
    assert result.value is None


def test_source_empty_list():
    result: Result = dig(keypath=["foo"], source=[])
    assert result.found is False
    assert result.value is None



def test_source_is_none():
    result: Result = dig(keypath=["foo"], source=cast(dict, None))
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
    source = [9,8,7]

    # when
    result: Result = dig(keypath=[1], source=source)

    # then
    assert result.value == 8
    assert result.found is True


def test_simple_list_negative_index():
    # given
    source = [9,8,7]

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


def test_index_out_of_range():
    # given
    source = [9,8,7]

    # when
    result = dig(keypath=[3], source=source)

    # then
    assert result.value is None
    assert result.found is False


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
    with open('tests/fixtures/sample.json') as fp:
        sample = json.load(fp)

    return sample


def test_complex_json_array(sample_json):
    # given
    keypath = [2, 'commit', 'author', 'date']

    # when
    result: Result = dig(keypath=keypath, source=sample_json)

    # then
    assert result.found is True
    assert result.value == "2024-08-21T23:17:54Z"

