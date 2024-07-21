import json
from abc import ABC, abstractmethod
from typing import List, Dict
import os

class Storage(ABC):
    @abstractmethod
    def save(self, data: List[Dict]):
        pass

class JSONStorage(Storage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: List[Dict]):
        existing_data = []
        
        # Check if file exists and is not empty
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            try:
                with open(self.file_path, 'r') as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode existing JSON in {self.file_path}. Starting with empty list.")

        # Ensure existing_data is a list
        if not isinstance(existing_data, list):
            existing_data = []

        for product in data:
            if product not in existing_data:
                existing_data.append(product)

        with open(self.file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)