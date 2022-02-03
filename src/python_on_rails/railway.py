from functools import reduce
from .common import identity
from .result import Result, unwrap


class Railway:
    def __init__(self, *steps):
        self.steps = steps

    def run(self, initial=None, success_handler=unwrap, failure_handler=identity):
        result = reduce(self.advance, self.steps, Result.success(initial))
        return success_handler(result) if result.is_success() else failure_handler(result)

    @staticmethod
    def advance(result, step):
        """
        Calls step with the unwrapped value of the current Result unless it is an error.
        The step function needs to accept a single argument, the unwrapped value,
        and return a new Result object.
        """
        return step(result.value) if result.is_success() else result
