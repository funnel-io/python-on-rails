from python_on_rails.common import identity
from python_on_rails.railway import Railway
from python_on_rails.result import as_result


def test_working_process():
    result = Railway(download, parse, output).run(success_handler=identity)
    assert result.is_success()
    assert result.value == {"data": {"rows": [["2022-01-19", 13], ["2022-01-20", 37]]}}


def test_failed_first_step():
    result = Railway(failed_download, parse, output).run()
    assert result.is_failure()
    assert isinstance(result.error, RuntimeError)
    assert repr(result.error) == "RuntimeError('Failed to download')"


def test_failed_middle_step():
    result = Railway(download, failed_parse, output).run()
    assert result.is_failure()
    assert isinstance(result.error, RuntimeError)
    assert repr(result.error) == "RuntimeError('Failed to parse')"


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


@as_result(RuntimeError)
def failed_parse(result):
    raise RuntimeError("Failed to parse")
