import json
import os
from utils.io_utils import read_input_jsons


def test_read_input_jsons_handles_valid_empty_invalid(tmp_path, capsys):
    input_dir = tmp_path / "input_jsons"
    input_dir.mkdir()

    # valid json
    valid_path = input_dir / "valid.json"
    valid_path.write_text(json.dumps({"a": 1}), encoding="utf-8")

    # empty file
    empty_path = input_dir / "empty.json"
    empty_path.write_text("", encoding="utf-8")

    # invalid json
    invalid_path = input_dir / "invalid.json"
    invalid_path.write_text("{ not json }", encoding="utf-8")

    # non-json file should be ignored
    (input_dir / "note.txt").write_text("hello", encoding="utf-8")

    (files_data, invalid_files) = read_input_jsons(str(input_dir))

    # one valid file loaded
    assert len(files_data) == 1
    assert files_data[0][0] == "valid.json"
    assert files_data[0][1] == {"a": 1}

    # only invalid json file detected (empty files are printed but not tracked)
    assert set(invalid_files) == {"invalid.json"}

    out = capsys.readouterr().out
    # Messages printed for empty and invalid
    assert "Файл пустой: empty.json" in out
    assert "Файл не в формате JSON или поврежден: invalid.json" in out


