from typing import Any
from main.domain.batch import Batch


class BatchRepositoryBase:

    def add(self, *, batch: Batch) -> Any:
        raise NotImplementedError

    def get(self, *, reference: str) -> Batch:
        raise NotImplementedError
