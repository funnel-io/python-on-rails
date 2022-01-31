from python_on_rails.catch import catch
from python_on_rails.railway import Railway, identity


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


@catch()
def failed_parse(result):
    raise RuntimeError("Failed to parse")
