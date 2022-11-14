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


def as_result(*exceptions):
    """
    Returns a decorator that handles the specified types of exceptions, if any are given.

    If the decorated function raises a handled exception, it will be caught
    and a Result object with its error property set will be returned.

    If the decorated function does not raise an error and does not return a
    Result object, a Result object with its value property set will be returned.
    """
    return catch(*exceptions, result_class=Result, failure=Result.failure, success=Result.success)


def failure(error):
    """
    >>> failure("some error")
    <Result error='some error' value=None>
    """
    return Result.failure(error)


def success(value):
    """
    >>> success("great success")
    <Result error=None value='great success'>
    """
    return Result.success(value)


def unwrap(result):
    return result.value
