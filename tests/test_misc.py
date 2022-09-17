from mlog._misc import extract_args_dict


def test_extract_args_dict():
    def wrap(a, b, c, d):
        pass

    mapping = extract_args_dict(wrap, 2, 3, 4, d=2)

    assert list(mapping.keys()) == ["a", "b", "c", "d"]
    assert list(mapping.values()) == [2, 3, 4, 2]
