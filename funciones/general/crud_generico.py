import json
import os
from typing import Dict, Any

class JsonBasicCRUD:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

    def _read(self) -> Dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # CREATE
    def create(self, key: str, value: Dict[str, Any]) -> bool:
        data = self._read()
        if key in data:
            return False  # ya existe
        data[key] = value
        self._write(data)
        return True

    # READ ALL
    def read_all(self) -> Dict[str, Any]:
        return self._read()

    # READ ONE
    def read(self, key: str):
        return self._read().get(key)

    # UPDATE
    def update(self, key: str, new_data: Dict[str, Any]) -> bool:
        data = self._read()
        if key not in data:
            return False
        data[key].update(new_data)
        self._write(data)
        return True

    # DELETE
    def delete(self, key: str) -> bool:
        data = self._read()
        if key not in data:
            return False
        del data[key]
        self._write(data)
        return True
