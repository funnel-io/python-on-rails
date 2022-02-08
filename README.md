# Python on Rails

![PyPI](https://img.shields.io/pypi/v/python-on-rails)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-on-rails)
![PyPI - Status](https://img.shields.io/pypi/status/python-on-rails)
![PyPI - License](https://img.shields.io/pypi/l/python-on-rails)
[![Python package](https://github.com/funnel-io/python-on-rails/actions/workflows/python-package.yml/badge.svg)](https://github.com/funnel-io/python-on-rails/actions/workflows/python-package.yml)

A library for supporting Railway-Oriented Programming in Python.

## Installation

Install the package `python_on_rails` version `1.0+` from PyPi.
The recommended `requirements.txt` line is `python_on_rails~=1.0`.
This package uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

## Code example
Below is an example to get started. Define functions ("railway stops") and wrap the return object into a `Result.success` (or `Result.failure`) object.
Create a `Railway` object and add your stops to it, finally call `run()`.

```python
from python_on_rails.railway import Railway
from python_on_rails.result import Result

def download(url):
    # fetch data from url...
    return Result.success(
        [
            {"date": "2022-01-19", "clicks": 13},
            {"date": "2022-01-20", "clicks": 37},
        ]
    )

def parse(downloaded_data):
    return Result.success([[entity["date"], entity["clicks"]] for entity in downloaded_data])

def output(parsed_data):
    return Result.success({"data": {"rows": parsed_data}})

result = Railway(download, parse, output).run()
print(f"{result=}")
```

Wrapping the return object can be omitted if you use `as_result` decorator from `result` module. Please see [railway_catch_test.py](tests/railway_catch_test.py) for example. 

## `railway` module

### `Railway` (class)

Combined with `Result` objects, a means of Railway-Oriented Programming.
A `Railway` object represents a process comprising of a number of steps. It accepts a number of steps, each of which should be a function that accepts and returns a `Result` object.

#### `run` (instance method)

Triggers the process. If an `initial` value is not supplied, the first step will be called with a `Result.success(None)`.

By default, if the process completes successfully, the final result will be unwrapped. If it fails however, a `Result` object with its error set will be returned. This behaviour can be configured by passing the optional `success_handler` and `failure_handler`. Those handlers are both functions that accept a single argument - a `Result` object.

## `result` module

### `Result` (class)

An object encapsulating a `value` or an `error`.

#### `is_failure` and `is_success` (instance methods)

Predicate methods denoting whether the result object has its error or value set.

#### `Result.failure` and `Result.success` (class methods)

Constructors that creates a `Result` object with either its error or value set.

#### `as_result` (function)

Convenience decorator builder applying the `Result` object to the generic `catch` decorator. Accepts any number of exceptions to catch and turn into `Result` objects.


#### `failure` (function)

Convenience function for creating a Result object with its error set.
Has the same effect as calling the `Result.failure` constructor.

#### `success` (function)

Convenience function for creating a Result object with its value set.
Has the same effect as calling the `Result.success` constructor.

#### `unwrap` (function)

Convenience function for extracting the value from a Result object.

## `either` module

### `Either`, `Failure`, and `Success` (classes)

An implementation of the [either](https://wiki.haskell.org/Typeclassopedia#Instances) [monad](https://en.wikipedia.org/wiki/Monad_(functional_programming)). The abstract `Either` base class encapsulates a value and is implemented as the `Success` and `Failure` classes.

#### `bind` (instance method)

Accepts a monadic function that takes a single argument and returns either a `Success` or a `Failure`.

For a `Success`, calls the supplied function with the unwrapped argument, returning its result.
For a `Failure`, ignores the supplied function and returns the existing failure.

#### `as_either` (function)

Convenience decorator builder applying the `Either` monad to the generic `catch` decorator. Accepts any number of exceptions to catch and turn into `Failure` objects.

## `common` module

### `catch` (function)

A decorator builder that ensures that the result of calling a function is returned as a `Result` object. Given a list of exceptions, catches those and wraps them into a `Result` object with its error set.

Can optionally be configured to handle and use the `Either` monad instead by passing the `result_class`, `failure`, and `success` arguments.

### `identity` (function)

The [identity function](https://en.wikipedia.org/wiki/Identity_function).
