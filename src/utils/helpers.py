import json
import os
from constants import PROGRESS_FILE


def load_progress():

    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)

    if not os.path.exists(PROGRESS_FILE):
        # Создаем начальный прогресс
        initial_progress = {"unlocked": [1], "disks": {}}
        save_progress(initial_progress)
        return initial_progress

    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)



def save_progress(progress_data):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f)
