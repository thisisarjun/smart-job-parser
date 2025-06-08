from abc import ABC, abstractmethod
from typing import Any, List

from src.vector_store.models import JobVectorStore


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> List[JobVectorStore]:
        pass
