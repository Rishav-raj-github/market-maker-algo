import unittest
from core.orderbook import OrderBook, Order

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.ob = OrderBook()

    def test_add_buy_order(self):
        o = Order('1', 'buy', 100.0, 10.0)
        self.ob.add_order(o)
        self.assertEqual(self.ob.get_best_bid(), 100.0)

    def test_add_sell_order(self):
        o = Order('2', 'sell', 101.0, 5.0)
        self.ob.add_order(o)
        self.assertEqual(self.ob.get_best_ask(), 101.0)

    def test_cancel_order(self):
        o = Order('1', 'buy', 100.0, 10.0)
        self.ob.add_order(o)
        self.ob.cancel_order('1')
        self.assertEqual(self.ob.get_best_bid(), 0.0)

if __name__ == '__main__':
    unittest.main()
