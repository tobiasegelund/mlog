import time

class Trace:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.function(*args, **kwargs)
        end_time = time.time()
        print("Execution took {} seconds".format(end_time-start_time))
        return result        # before function


# @Tracing
# def get_square(n):
#     print("given number is:", n)
#     return n * n

# print("Square of number is:", get_square(195))
