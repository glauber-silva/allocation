from main.domain.batch import Batch


def test_repository_can_save_a_batch(app):
    batch = Batch(ref="batch1", sku="RUSTY-SOAPDISH", qty=100, eta=None)

    repository = SqlAlchemyBatchRepository()
    repository.add(batch=batch)
    
    rows = list(db.session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches" '
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
