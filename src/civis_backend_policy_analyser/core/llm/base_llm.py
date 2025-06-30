from abc import ABC, abstractmethod

class BaseLLMModel(ABC):
    @abstractmethod
    def get_llm(self):
        pass
