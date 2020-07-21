def test_red(test_client):
    from server import red

    red.set('fff', b'hello')

    assert red.get('fff') == b'hello'