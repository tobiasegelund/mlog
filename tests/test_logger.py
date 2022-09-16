def test_function_with_parenthesis(logger):
    @logger.log()
    def test_func():
        print()


def test_function_without_parenthesis(logger):
    @logger.log
    def test_func():
        print()


def test_method_with_parenthsis(logger):
    class Method:
        @logger.log()
        def test_method_with_parenthsis(self, logger):
            print()


def test_method_without_parenthsis(logger):
    class Method:
        @logger.log
        def test_method_with_parenthsis(self, logger):
            print()
