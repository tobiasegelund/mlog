from mlog._format import marshalling_dict, marshalling_kwargs


def test_marshalling_kwargs():
    mapping = marshalling_kwargs(a=2, b=3)
    assert mapping == '{"a": 2, "b": 3}'


def test_marshalling_dict():
    d = {
        "a": 2,
        "b": 3,
    }
    mapping = marshalling_dict(d)
    assert mapping == '{"a": 2, "b": 3}'
