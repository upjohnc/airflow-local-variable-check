import io
from pathlib import Path

import jmespath

from airflow_hook import check_local_test_items as check


def test_assert_true(monkeypatch):
    file_stuff = 'with snf.connect() \nassert'
    monkeypatch.setattr(check.Path, 'open', lambda x: io.StringIO(file_stuff))
    result = check.check_assert_in_file(Path('aoeu'))

    assert result is None


def test_assert_bad(monkeypatch):
    file_stuff = 'with snf.connect() \nonenoftheassert'
    file_name = 'fake'
    monkeypatch.setattr(check.Path, 'open', lambda x: io.StringIO(file_stuff))
    result = check.check_assert_in_file(Path(file_name))

    assert file_name in result.keys()
    assert len(jmespath.search(file_name, result)) == 1
    result_file_info = jmespath.search(file_name, result)[0]
    assert 'line' in result_file_info.keys() and 'line_number' in result_file_info.keys()
