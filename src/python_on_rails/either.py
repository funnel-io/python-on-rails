class Either:
    def __init__(self, value):
        self.value = value

    def bind(self, func):
        """
        Accepts a monadic function that returns either a Success or a Failure.
        """
        raise NotImplementedError

    def __call__(self, func):
        return self.bind(func)

    def __or__(self, func):
        return self.bind(func)

    def __repr__(self):
        return f"<{self.__class__.__name__} value={repr(self.value)}>"


class Success(Either):
    def bind(self, func):
        """
        Calls the bound function with the unwrapped value.
        The bound function is expected to return either a Success or a Failure.

        >>> Success(1.23).bind(lambda value: Success(int(value))).value
        1
        """
        return func(self.value)


class Failure(Either):
    def bind(self, func):
        """
        Ignores the supplied function and returns itself.

        >>> Failure(1.23).bind(int).value
        1.23
        """
        return self
