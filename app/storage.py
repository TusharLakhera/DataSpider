import json
from abc import ABC, abstractmethod
from typing import List, Dict

class Storage(ABC):
    @abstractmethod
    def save(self, data: List[Dict]):
        pass

class JSONStorage(Storage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: List[Dict]):
        try:
            with open(self.file_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        for product in data:
            if product not in existing_data:
                existing_data.append(product)

        with open(self.file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)