from pathlib import Path
import subprocess
import sys

import pytest

from sqs_lambda import app


@pytest.mark.parametrize("bodies", [[], ["hello"], ["first", "second"]])
def test_lambda_handler_processes_sqs_records(bodies, capsys):
    event = {"Records": [{"body": body} for body in bodies]}

    assert app.lambda_handler(event, None) is None
    assert capsys.readouterr().out == "".join(body + "\n" for body in bodies)


def test_lambda_handler_runs_without_third_party_dependencies():
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            "-c",
            "from sqs_lambda import app; "
            "app.lambda_handler({'Records': [{'body': 'hello'}]}, None)",
        ],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout == "hello\n"
    assert result.stderr == ""
