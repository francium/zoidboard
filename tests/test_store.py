from dsb.store import RingerBuffer, Store


class TestRingBuffer:
    def test_insert_items(self):
        ring = RingerBuffer(4)
        ring.push(1)
        assert ring.read() == [1]
        ring.push(2)
        assert ring.read() == [1, 2]

    def test_fill_buffer(self):
        ring = RingerBuffer(4)
        ring.push(1)
        ring.push(2)
        ring.push(3)
        ring.push(4)
        assert ring.read() == [1, 2, 3, 4]

    def test_over_fill_buffer(self):
        ring = RingerBuffer(4)
        ring.push(1)
        ring.push(2)
        ring.push(3)
        ring.push(4)
        ring.push(5)
        assert ring.read() == [2, 3, 4, 5]
        ring.push(6)
        assert ring.read() == [3, 4, 5, 6]


class TestStore:
    def test_add_and_get_item_scalar(self):
        store = Store()
        store.register('foo', 'scalar')
        store.update('foo', 55)
        assert store.get('foo') == 55

    def test_add_and_get_item_vector(self):
        store = Store()
        store.register('foo', 'vector')
        store.update('foo', 55)
        assert store.get('foo') == [55]

    def test_add_multiple_items_to_vector_bin(self):
        store = Store()
        store.register('foo', 'vector')
        store.update('foo', 1)
        store.update('foo', 2)
        assert store.get('foo') == [1, 2]