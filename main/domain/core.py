from typing import List

from src.domain.batch import OrderLine, Batch
from src.domain.exception import OutOfStock


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line=line)
        )
        batch.allocate(line=line)
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
    return batch.reference