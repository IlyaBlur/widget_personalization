import json
import os
import builtins
from processing.pipeline import run_processing


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def test_pipeline_aborts_on_invalid_json(tmp_path, capsys, monkeypatch):
    in_dir = tmp_path / "input_jsons"
    out_dir = tmp_path / "output_jsons"
    in_dir.mkdir()
    # invalid json
    (in_dir / "bad.json").write_text("{ not json }", encoding="utf-8")

    # any prompt value should be ignored due to early abort
    monkeypatch.setattr(builtins, "input", lambda *args: "1")

    run_processing(str(in_dir), str(out_dir))

    out = capsys.readouterr().out
    assert "Найдены некорректные JSON файлы" in out
    assert "- bad.json" in out
    assert not os.path.exists(out_dir)


def test_pipeline_remove_and_merge(tmp_path, monkeypatch):
    in_dir = tmp_path / "input_jsons"
    out_dir = tmp_path / "output_jsons"
    in_dir.mkdir()
    data = {
        "widgets": [
            {"segment": "S", "widgets": [{"id": "a"}, {"id": "b"}]}
        ]
    }
    write_json(in_dir / "one.json", data)
    write_json(in_dir / "two.json", data)

    # choose remove, ids to remove: a
    inputs = iter(["1", "a"])  # action remove, ids
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))

    run_processing(str(in_dir), str(out_dir))

    merged = json.loads((out_dir / "new_merged.json").read_text(encoding="utf-8"))
    ids = [w["id"] for w in merged["widgets"][0]["widgets"]]
    assert ids == ["b"]


def test_pipeline_add_reports_missing_segments(tmp_path, capsys, monkeypatch):
    in_dir = tmp_path / "input_jsons"
    out_dir = tmp_path / "output_jsons"
    in_dir.mkdir()
    data = {
        "widgets": [
            {"segment": "A", "widgets": [{"id": "anchor"}]},
            {"segment": "B", "widgets": [{"id": "x"}]},
        ]
    }
    write_json(in_dir / "one.json", data)

    payload = [{"id": "n"}]
    inputs = iter(["2", "anchor", json.dumps(payload)])
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))

    run_processing(str(in_dir), str(out_dir))

    out = capsys.readouterr().out
    assert 'one.json | B - не получилось добавить, т.к. отсутствует виджет "anchor"' in out
    # single file => _new.json output should exist
    assert (out_dir / "one_new.json").exists()


