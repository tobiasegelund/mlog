import pytest


def test_wrapper(logger):
    @logger.log()
    def test_func():
        print()


# class TestMethod:
#     @logger.log()
#     def test_method(self, logger):
#         print()
