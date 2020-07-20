import pytest

from src.domain.core import allocate
from src.domain.exception import OutOfStock
from tests.domain.test_batch import tomorrow, today, later
from src.domain.batch import Batch, OrderLine


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch(
        ref="in-stock-batch",
        sku="RETRO-CLOK",
        qty=100,
        eta=None
    )

    shipment_batch = Batch(
        ref="shipment-batch",
        sku="RETRO-CLOCK",
        qty=100,
        eta=tomorrow
    )

    line = OrderLine(orderid="oref", sku="RETRO-CLOCK", qty=10)
    allocate(line=line, batches=[in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefer_ealier_batches():
    ealiest = Batch(ref="speedy-batch", sku="MINIMALIST-SPOON", qty=100, eta=today)
    medium = Batch(ref="normal-batch", sku="MINIMALIST-SPOON", qty=100, eta=tomorrow)
    latest = Batch(ref="normal-batch", sku="MINIMALIST-SPOON", qty=100, eta=later)

    line = OrderLine(orderid='order1', sku="MINIMALIST-SPOON", qty=10)
    allocate(line=line, batches=[medium, ealiest, latest])
    assert ealiest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocate_batch_ref():
    in_stock_batch = Batch(ref="in-stock-batch-ref", sku="HIGHBROW-POSTER", qty=100, eta=None)
    shipment_batch = Batch(ref="shipment-batch-ref", sku="HIGHBROW-POSTER", qty=100, eta=tomorrow)
    line = OrderLine(orderid="oref", sku="HIGHBROW-POSTER", qty=10)
    allocation = allocate(line=line, batches=[in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_stock_exception_if_cannot_allocate():
    batch = Batch(ref="BATCH-1", sku="SMALL-FORK", qty=10, eta=today)
    allocate(line=OrderLine(orderid="ORDER1", sku="SMALL-FORK", qty=10), batches=[batch])
    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(line=OrderLine(orderid="ORDER2", sku="SMALL-FORK", qty=1), batches=[batch])
