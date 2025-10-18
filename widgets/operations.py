import copy
from typing import Dict, Any, List, Tuple, Set, Iterable


def insert_widget_after(data: Dict[str, Any], after_id: str, widget_to_insert: Dict[str, Any]) -> Dict[str, Any]:
    for segment in data.get("widgets", []):
        widgets = segment.get("widgets", [])
        new_widgets = []
        for widget in widgets:
            new_widgets.append(widget)
            if widget.get("id") == after_id:
                new_widgets.append(copy.deepcopy(widget_to_insert))
        segment["widgets"] = new_widgets
    return data


def insert_widgets(data: Dict[str, Any], spec: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    after_id = (spec or {}).get("after_id", "")
    result = copy.deepcopy(data)
    missing_in_segments: List[str] = []

    # Even if there are no widgets to add (e.g., invalid JSON in prompt),
    # we still want to validate and report segments missing the anchor.
    if not spec or not spec.get("widgets"):
        if after_id:
            for segment in result.get("widgets", []):
                segment_widgets = segment.get("widgets", [])
                has_anchor = any(w.get("id") == after_id for w in segment_widgets)
                if not has_anchor:
                    missing_in_segments.append(segment.get("segment"))
        return result, missing_in_segments

    # We need to detect per segment if after_id exists
    widgets_to_add: Iterable[Dict[str, Any]] = spec["widgets"]
    for segment in result.get("widgets", []):
        segment_widgets = segment.get("widgets", [])
        has_anchor = any(w.get("id") == after_id for w in segment_widgets)
        if not has_anchor:
            missing_in_segments.append(segment.get("segment"))
            continue
        # Insert each requested widget after the anchor, preserving order and duplicating after each anchor occurrence
        new_widgets: List[Dict[str, Any]] = []
        for w in segment_widgets:
            new_widgets.append(w)
            if w.get("id") == after_id:
                for to_add in widgets_to_add:
                    new_widgets.append(copy.deepcopy(to_add))
        segment["widgets"] = new_widgets

    return result, missing_in_segments


def remove_widgets(data: Dict[str, Any], widget_ids_to_remove: Set[str]) -> Dict[str, Any]:
    for segment in data.get("widgets", []):
        widgets = segment.get("widgets", [])
        segment["widgets"] = [w for w in widgets if w.get("id") not in widget_ids_to_remove]
    return data


def get_segments_full_signature(data: Dict[str, Any]) -> List[Tuple[str, Tuple[Tuple[str, Any, Any], ...]]]:
    signature: List[Tuple[str, Tuple[Tuple[str, Any, Any], ...]]] = []
    for seg in data.get("widgets", []):
        widgets_info = tuple((w.get("id"), w.get("customizable"), w.get("title")) for w in seg.get("widgets", []))
        signature.append((seg.get("segment"), widgets_info))
    return signature


