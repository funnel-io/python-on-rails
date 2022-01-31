from python_on_rails.railway import Railway, identity
from python_on_rails.result import Result


def test_working_process_unwraps_the_final_result():
    result = Railway(download, parse, output).run()
    assert result == {"data": {"rows": [["2022-01-19", 13], ["2022-01-20", 37]]}}


def test_working_process_without_unwrapping_the_final_result():
    result = Railway(download, parse, output).run(success_handler=identity)
    assert result.is_success()
    assert result.value == {"data": {"rows": [["2022-01-19", 13], ["2022-01-20", 37]]}}


def test_failed_first_step():
    result = Railway(failed_download, parse, output).run()
    assert result.is_failure()
    assert result.error == "Failed to download"


def test_failed_middle_step():
    result = Railway(download, failed_parse, output).run()
    assert result.is_failure()
    assert result.error == "Failed to parse"


def download(result):
    return Result.success(
        [
            {"date": "2022-01-19", "clicks": 13},
            {"date": "2022-01-20", "clicks": 37},
        ]
    )


def parse(result):
    return Result.success([[entity["date"], entity["clicks"]] for entity in result])


def output(result):
    return Result.success({"data": {"rows": result}})


def failed_download(result):
    return Result.failure("Failed to download")


def failed_parse(result):
    return Result.failure("Failed to parse")
