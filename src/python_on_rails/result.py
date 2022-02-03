from functools import partial
from .common import catch


class Result:
    def __init__(self, error=None, value=None):
        self.error = error
        self.value = value

    @classmethod
    def failure(cls, error):
        return cls(error=error)

    @classmethod
    def success(cls, value):
        return cls(value=value)

    def is_failure(self):
        return bool(self.error)

    def is_success(self):
        return not self.is_failure()

    def __repr__(self):
        return f"<{self.__class__.__name__} error={repr(self.error)} value={repr(self.value)}>"


as_result = partial(catch, result_class=Result, failure=Result.failure, success=Result.success)


def failure(error):
    return Result.failure(error)


def success(value):
    return Result.success(value)


def unwrap(result):
    return result.value
