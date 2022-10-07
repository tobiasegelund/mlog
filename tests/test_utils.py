from mlog._utils import map_args, is_method


def test_map_args():
    def wrap(a, b, c, d):
        pass

    mapping = map_args(wrap, 2, 3, 4, d=2)

    assert list(mapping.keys()) == ["a", "b", "c", "d"]
    assert list(mapping.values()) == [2, 3, 4, 2]


def test_is_method():
    def function():
        pass

    class Test:
        def method(self):
            pass

    assert is_method(Test.method) == True
    assert is_method(function) == False
