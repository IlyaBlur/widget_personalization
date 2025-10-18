from widgets.operations import remove_widgets, insert_widgets, get_segments_full_signature


def sample_data():
    return {
        "widgets": [
            {
                "segment": "A",
                "widgets": [
                    {"id": "x"},
                    {"id": "anchor"},
                    {"id": "y"},
                ],
            },
            {
                "segment": "B",
                "widgets": [
                    {"id": "x"},
                    {"id": "y"},
                ],
            },
        ]
    }


def test_remove_widgets():
    data = sample_data()
    updated = remove_widgets(data, {"x"})
    assert all(all(w.get("id") != "x" for w in seg["widgets"]) for seg in updated["widgets"])


def test_insert_widgets_with_missing_segments_report():
    data = sample_data()
    spec = {"after_id": "anchor", "widgets": [{"id": "new1"}, {"id": "new2"}]}
    updated, missing = insert_widgets(data, spec)
    # Segment A has anchor, B does not
    assert set(missing) == {"B"}
    a_widgets = [w["id"] for w in updated["widgets"][0]["widgets"]]
    assert a_widgets == ["x", "anchor", "new1", "new2", "y"]


def test_insert_widgets_validates_even_if_no_widgets():
    data = sample_data()
    spec = {"after_id": "anchor", "widgets": []}
    updated, missing = insert_widgets(data, spec)
    assert set(missing) == {"B"}
    # unchanged layout
    assert updated["widgets"][0]["widgets"][1]["id"] == "anchor"


def test_signature_generation_stable():
    data = sample_data()
    sig = get_segments_full_signature(data)
    assert isinstance(sig, list)
    assert sig[0][0] == "A"

