import json
import os
from constants import PROGRESS_FILE


def load_progress():
    """Загружает прогресс из файла (DRY - переиспользуемая функция)"""
    try:
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)

        if not os.path.exists(PROGRESS_FILE):
            # Создаем начальный прогресс
            initial_progress = {"unlocked": [1], "disks": {}}
            save_progress(initial_progress)
            return initial_progress

        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки прогресса: {e}")
        return {"unlocked": [1], "disks": {}}


def save_progress(progress_data):
    """Сохраняет прогресс в файл"""
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f)
    except Exception as e:
        print(f"Ошибка сохранения прогресса: {e}")