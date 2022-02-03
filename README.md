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

## Current Functionality

### `Railway`

Combined with `Result` objects, a means of Railway-Oriented Programming.
A `Railway` object represents a process comprising of a number of steps. It accepts a number of steps, each of which should be a function that accepts and returns a `Result` object.

#### `run`

Triggers the process. If an `initial` value is not supplied, the first step will be called with a `Result.success(None)`.

By default, if the process completes successfully, the final result will be unwrapped. If it fails however, a `Result` object with its error set will be returned. This behaviour can be configured by passing the optional `success_handler` and `failure_handler`. Those handlers are both functions that accept a single argument - a `Result` object.


### `Result`

An object encapsulating a `value` or an `error`.

#### `is_failure` and `is_success` (instante methods)

Predicate methods denoting whether the result object has its error or value set.

#### `Result.failure` and `Result.success` (class methods)

Constructors that creates a `Result` object with either its error or value set.

#### `as_result` (decorator function)

Convenience decorator function applying the `Result` object to the generic `catch` decorator. Accepts any number of exceptions to catch and turn into `Result` objects.


#### `failure` (function)

Convenience function for creating a Result object with its error set.
Has the same effect as calling the `Result.failure` constructor.

#### `success` (function)

Convenience function for creating a Result object with its value set.
Has the same effect as calling the `Result.success` constructor.

#### `unwrap` (function)

Convenience function for extracting the value from a Result object.


### `Either`

An implementation of the [either monad](). The abstract `Either` base class encapsulates a value and is implemented as the `Success` and `Failure` classes.

#### `bind` (instance method)

Accepts a monadic function that takes a single argument and returns either a `Success` or a `Failure`.

For a `Success`, calls the supplied function with the unwrapped argument, returning its result.
For a `Failure`, ignores the supplied function and returns the existing failure.

#### `as_either` (decorator function)

Convenience decorator function applying the `Either` monad to the generic `catch` decorator. Accepts any number of exceptions to catch and turn into `Failure` objects.


### `catch`

A decorator builder that ensures that the result of calling a function is returned as a `Result` object. Given a list of exceptions, catches those and wraps them into a `Result` object with its error set.

Can optionally be configured to handle and use the `Either` monad instead by passing the `result_class`, `failure`, and `success` arguments.
