from functools import wraps


def identity(result):
    return result


def catch(*exceptions, result_class=object, failure=identity, success=identity):
    """
    Returns a decorator that handles the specified types of exceptions.
    If no exceptions are given, defaults to Exception.

    If the decorated function raises a handled exception, it will be caught
    and passed on to the failure callback function before being returned.
    By default, a Result object with its error property set will be returned.

    If the decorated function does not raise an error and does not return a
    result_class object, its result will be passed to the success callback function
    before being returned.
    By default, a Result object with its value property set will be returned.
    """
    exceptions = exceptions or Exception

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result if isinstance(result, result_class) else success(result)
            except exceptions as e:
                return failure(e)

        return wrapper

    return decorator
