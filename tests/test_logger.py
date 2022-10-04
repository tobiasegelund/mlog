def test_input_function_with_parenthesis(logger):
    @logger.input.log()
    def test_func():
        print()


def test_input_function_without_parenthesis(logger):
    @logger.input.log
    def test_func():
        print()


def test_input_method_with_parenthsis(logger):
    class Method:
        @logger.input.log()
        def test_method_with_parenthsis(self, logger):
            print()


def test_input_method_without_parenthsis(logger):
    class Method:
        @logger.input.log
        def test_method_with_parenthsis(self, logger):
            print()


def test_output_function_with_parenthesis(logger):
    @logger.output.log()
    def test_func():
        print()


def test_output_function_without_parenthesis(logger):
    @logger.output.log
    def test_func():
        print()


def test_output_method_with_parenthsis(logger):
    class Method:
        @logger.output.log()
        def test_method_with_parenthsis(self, logger):
            print()


def test_output_method_without_parenthsis(logger):
    class Method:
        @logger.output.log
        def test_method_with_parenthsis(self, logger):
            print()


def test_profile_function_with_parenthesis(logger):
    @logger.profile.log()
    def test_func():
        print()


def test_profile_function_without_parenthesis(logger):
    @logger.profile.log
    def test_func():
        print()


def test_profile_method_with_parenthsis(logger):
    class Method:
        @logger.profile.log()
        def test_method_with_parenthsis(self, logger):
            print()


def test_profile_method_without_parenthsis(logger):
    class Method:
        @logger.profile.log
        def test_method_with_parenthsis(self, logger):
            print()
