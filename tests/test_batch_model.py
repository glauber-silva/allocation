def test_orderline_mapper_can_load_lines(session):

    session.execute(
        f'INSERT INTO order_Lines (order_id, sku, qty) VALUES'
        f'("ORDER-1", "RED-CHAIR", 12),'
        f'("ORDER-1", "RED-TABLE", 13),'
        f'("ORDER-2", "BLUE-LIPSTICK", 14),'

    )

    expected = [
        model.OrderLine("ORDER-1", "RED-CHAIR", 12),
        model.OrderLine("ORDER-1", "RED-TABLE", 13),
        model.OrderLine("ORDER-2", "BLUE-LIPSTICK", 14)
    ]
   
   assert session.query(model.OrderLine.all()) == expected


def test_orderline_mapper_can_save_line(session):
    new_line = model.OrderLine("ORDER-1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()
    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("ORDER-1", "DECORATIVE-WIDGET", 12)]

    