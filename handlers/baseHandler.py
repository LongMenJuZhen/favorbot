from abc import ABC, abstractmethod

class BaseHandler(ABC):

    @abstractmethod
    def handle(self, s):
        pass