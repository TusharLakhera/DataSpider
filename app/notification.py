from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class ConsoleNotification(Notification):
    def send(self, message: str):
        print(message)