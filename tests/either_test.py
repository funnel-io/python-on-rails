import pytest
from python_on_rails.either import Either, Failure, Success


def add_one(x):
    if isinstance(x, int):
        return Success(x + 1)
    else:
        return Failure(f"Could not add 1 to '{x}'")


def times_five(x):
    return Success(x * 5)


def test_success_executes_bindings():
    result = Success(1).bind(add_one).bind(times_five)
    assert isinstance(result, Success)
    assert result.value == 10


def test_failure_does_not_execute_bindings():
    result = Failure(0).bind(add_one).bind(times_five)
    assert isinstance(result, Failure)
    assert result.value == 0


def test_a_failure_stops_the_execution_of_later_bindings():
    result = Success("NaN").bind(add_one).bind(times_five)
    assert isinstance(result, Failure)
    assert result.value == "Could not add 1 to 'NaN'"


def test_either_does_not_implement_bind():
    with pytest.raises(NotImplementedError):
        Either("way").bind(int)


def test_success_alias_call_to_bind():
    result = Success(1)(add_one)(times_five)
    assert isinstance(result, Success)
    assert result.value == 10


def test_failure_alias_call_to_bind():
    result = Failure(0)(add_one)(times_five)
    assert isinstance(result, Failure)
    assert result.value == 0


def test_success_alias_or_to_bind():
    result = Success(1) | add_one | times_five
    assert isinstance(result, Success)
    assert result.value == 10


def test_failure_alias_or_to_bind():
    result = Failure(0) | add_one | times_five
    assert isinstance(result, Failure)
    assert result.value == 0


def test_success_repr():
    assert repr(Success(1)) == "<Success value=1>"


def test_failure_repr():
    assert repr(Failure(RuntimeError("Boom!"))) == "<Failure value=RuntimeError('Boom!')>"


def test_either_repr():
    assert repr(Either(str.upper)) == "<Either value=<method 'upper' of 'str' objects>>"
