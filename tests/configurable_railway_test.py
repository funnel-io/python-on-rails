import pytest
from python_on_rails.catch import catch
from python_on_rails.railway import Railway


def test_failed_process_with_custom_error_handler():
    def raise_error(result):
        raise result.error

    with pytest.raises(RuntimeError, match="Failed to download"):
        Railway(failed_download, parse, output).run(failure_handler=raise_error)


@catch()
def download(result):
    return [{"date": "2022-01-19", "clicks": 13}, {"date": "2022-01-20", "clicks": 37}]


@catch()
def parse(result):
    return [[entity["date"], entity["clicks"]] for entity in result]


@catch()
def output(result):
    return {"data": {"rows": result}}


@catch(RuntimeError)
def failed_download(result):
    raise RuntimeError("Failed to download")
