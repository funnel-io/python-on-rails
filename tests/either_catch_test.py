from python_on_rails.either import as_either, Failure, Success


@as_either()
def add_one(x):
    return x + 1


@as_either()
def times_five(x):
    return x * 5


def test_success_executes_bindings():
    result = Success(1).bind(add_one).bind(times_five)
    assert isinstance(result, Success)
    assert result.value == 10


def test_a_failure_stops_the_execution_of_later_bindings():
    result = Success("NaN").bind(add_one).bind(times_five)
    assert isinstance(result, Failure)
    assert type(result.value) == TypeError
    assert repr(result.value) == "TypeError('can only concatenate str (not \"int\") to str')"
