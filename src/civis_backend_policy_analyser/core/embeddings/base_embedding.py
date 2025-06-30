from abc import ABC, abstractmethod

class BaseEmbeddingModel(ABC):
    @abstractmethod
    def get_embedding_model(self):
        pass
