import copy
from typing import List, Tuple, Dict, Any

from utils.io_utils import read_input_jsons, ensure_output_dir, write_single_output, write_merged_output, write_multiple_outputs
from utils.prompts import ask_action, ask_ids_to_remove, ask_widgets_to_add
from widgets.operations import remove_widgets, insert_widgets, get_segments_full_signature


def run_processing(input_folder: str, output_folder: str) -> None:
    files_data_raw = read_input_jsons(input_folder)
    # Backward compatibility if function signature hasn't been reloaded yet
    if isinstance(files_data_raw, tuple):
        files_data, invalid_files = files_data_raw
    else:
        files_data = files_data_raw  # type: ignore
        invalid_files = []

    if invalid_files:
        print("Найдены некорректные JSON файлы. Процесс остановлен. Исправьте следующие файлы:")
        for nf in invalid_files:
            print(f"- {nf}")
        return
    if len(files_data) == 0:
        print("Входные файлы не найдены или все файлы пустые/битые. Добавьте файлы в формате .json в папку input_jsons.")
        return

    action = ask_action()

    # Collect additional details based on action
    widget_ids_to_remove = []
    widgets_to_add_spec = None
    if action == "remove":
        widget_ids_to_remove = ask_ids_to_remove()
    elif action == "add":
        widgets_to_add_spec = ask_widgets_to_add()

    # Apply action per file
    processed: List[Tuple[str, Dict[str, Any]]] = []
    files_signatures: List[Any] = []
    for filename, data in files_data:
        if action == "remove":
            updated = remove_widgets(copy.deepcopy(data), set(widget_ids_to_remove))
        elif action == "add":
            updated, missing_segments = insert_widgets(copy.deepcopy(data), widgets_to_add_spec)
            if missing_segments:
                for seg in missing_segments:
                    print(f"{filename} | {seg} - не получилось добавить, т.к. отсутствует виджет \"{widgets_to_add_spec.get('after_id','')}\"")
        else:
            # no-op (should not happen due to prompt constraints)
            updated = copy.deepcopy(data)

        processed.append((filename, updated))
        files_signatures.append(get_segments_full_signature(updated))

    ensure_output_dir(output_folder)

    # Single file case
    if len(processed) == 1:
        write_single_output(output_folder, processed[0][0], processed[0][1])
        return

    # Compare signatures
    base_signature = files_signatures[0]
    all_match = all(sig == base_signature for sig in files_signatures[1:])

    if all_match:
        merged_data = copy.deepcopy(processed[0][1])
        write_merged_output(output_folder, merged_data)
    else:
        write_multiple_outputs(output_folder, processed)


