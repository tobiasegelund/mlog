def test_input_state_df(logger, df):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func(df)


def test_input_state_array(logger, array):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func(array)


def test_input_state_list(logger):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func([10, 20, 30])


def test_output_state(logger):
    @logger.output.log(metrics={"i": ["mean"]})
    def test_func(i=[10, 20, 30]):
        return i

    test_func()
