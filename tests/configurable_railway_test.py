from python_on_rails.result import as_result
from python_on_rails.railway import Railway


def test_failed_process_with_custom_error_handler():
    def handle_error(result):
        return (
            f"Got a <{result.error.__class__.__name__}> with the message '{result.error.args[0]}'"
        )

    result = Railway(failed_download, parse, output).run(failure_handler=handle_error)
    assert result == "Got a <RuntimeError> with the message 'Failed to download'"


@as_result()
def download(result):
    return [
        {"date": "2022-01-19", "clicks": 13},
        {"date": "2022-01-20", "clicks": 37},
    ]


@as_result()
def parse(result):
    return [[entity["date"], entity["clicks"]] for entity in result]


@as_result()
def output(result):
    return {"data": {"rows": result}}


@as_result(RuntimeError)
def failed_download(result):
    raise RuntimeError("Failed to download")
