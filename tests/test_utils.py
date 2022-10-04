from mlog._utils import map_args


def test_map_args():
    def wrap(a, b, c, d):
        pass

    mapping = map_args(wrap, 2, 3, 4, d=2)

    assert list(mapping.keys()) == ["a", "b", "c", "d"]
    assert list(mapping.values()) == [2, 3, 4, 2]
