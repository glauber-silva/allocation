from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:

    def __init__(self, *, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()
        
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, *, line: OrderLine):
        if self.can_allocate(line=line):
            self._allocations.add(line)

    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity (self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, *, line: OrderLine):
        if line.qty <= self.available_quantity and line.sku == self.sku:
            return True
        return False
