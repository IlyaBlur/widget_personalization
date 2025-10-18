import os
import json
from typing import List, Tuple, Dict, Any


def read_input_jsons(input_folder: str) -> Tuple[List[Tuple[str, Dict[str, Any]]], List[str]]:
    files_data: List[Tuple[str, Dict[str, Any]]] = []
    invalid_files: List[str] = []
    if not os.path.exists(input_folder):
        return files_data, invalid_files

    for filename in os.listdir(input_folder):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(input_folder, filename)
        try:
            if os.path.getsize(path) == 0:
                print(f"Файл пустой: {filename}")
                continue
        except OSError:
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Файл не в формате JSON или поврежден: {filename}")
            invalid_files.append(filename)
            continue
        files_data.append((filename, data))
    return files_data, invalid_files


def ensure_output_dir(output_folder: str) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def write_single_output(output_folder: str, filename: str, data: Dict[str, Any]) -> None:
    new_filename = os.path.splitext(filename)[0] + "_new.json"
    output_path = os.path.join(output_folder, new_filename)
    with open(output_path, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, ensure_ascii=False, indent=2)
    print(f"Обработан единственный файл. Создан новый файл: {new_filename}")


def write_merged_output(output_folder: str, merged_data: Dict[str, Any]) -> None:
    output_path = os.path.join(output_folder, "new_merged.json")
    with open(output_path, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, indent=2)
    print(f"Объединенный файл сохранен: {output_path}")


def write_multiple_outputs(output_folder: str, files_data: List[Tuple[str, Dict[str, Any]]]) -> None:
    print("Обнаружены различия в файлах. Создаются отдельные новые файлы:")
    for filename, data in files_data:
        new_filename = os.path.splitext(filename)[0] + "_new.json"
        output_path = os.path.join(output_folder, new_filename)
        with open(output_path, 'w', encoding='utf-8') as f_out:
            json.dump(data, f_out, ensure_ascii=False, indent=2)
        print(f"Создан новый файл: {new_filename}")


