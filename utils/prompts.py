from typing import List, Dict, Any


def ask_action() -> str:
    print("Выберите действие:")
    print("1 - Удалить виджеты по ID")
    print("2 - Добавить виджеты после указанного ID")
    choice = input("Введите номер операции (1/2) и нажмите Enter: ").strip()
    while choice not in ("1", "2"):
        choice = input("Неверный ввод. Введите 1 или 2: ").strip()
    return "remove" if choice == "1" else "add"


def ask_ids_to_remove() -> List[str]:
    raw = input("Введите ID виджетов для удаления через запятую: ").strip()
    ids = [x.strip() for x in raw.split(",") if x.strip()]
    if not ids:
        print("ID не указаны. Действие будет пропущено.")
    return ids


def ask_widgets_to_add() -> Dict[str, Any]:
    after_id = input("После какого ID вставлять? Введите ID: ").strip()
    print("Введите JSON массив виджетов для добавления (пример: [{\"id\":\"growthHackMain\",\"customizable\":true,\"title\":\"Виджет\"}]):")
    widgets_json = input().strip()
    import json
    try:
        widgets = json.loads(widgets_json)
        if not isinstance(widgets, list):
            raise ValueError
    except Exception:
        print("Неверный JSON. Добавление будет пропущено.")
        widgets = []
    return {"after_id": after_id, "widgets": widgets}


