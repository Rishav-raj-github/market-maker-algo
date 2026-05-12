import unittest
from core.risk_manager import RiskManager

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.rm = RiskManager(max_position=100.0, max_drawdown=500.0)

    def test_position_limit(self):
        self.assertTrue(self.rm.check_order_allowed('buy', 50.0))
        self.rm.update_position('buy', 60.0, 100.0)
        self.assertFalse(self.rm.check_order_allowed('buy', 50.0)) # 60 + 50 > 100

    def test_drawdown_limit(self):
        self.rm.update_pnl(100.0, 0.0) # Peak is 100
        self.rm.update_pnl(-450.0, 0.0) # Current is -450. Drawdown is 550.
        self.assertTrue(self.rm.is_drawdown_exceeded())

if __name__ == '__main__':
    unittest.main()
