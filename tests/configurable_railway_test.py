import pytest
from python_on_rails.result import as_result
from python_on_rails.railway import Railway


def test_failed_process_with_custom_error_handler():
    def raise_error(result):
        raise result.error

    with pytest.raises(RuntimeError, match="Failed to download"):
        Railway(failed_download, parse, output).run(failure_handler=raise_error)


@as_result()
def download(result):
    return [{"date": "2022-01-19", "clicks": 13}, {"date": "2022-01-20", "clicks": 37}]


@as_result()
def parse(result):
    return [[entity["date"], entity["clicks"]] for entity in result]


@as_result()
def output(result):
    return {"data": {"rows": result}}


@as_result(RuntimeError)
def failed_download(result):
    raise RuntimeError("Failed to download")
