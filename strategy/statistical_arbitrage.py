import numpy as np
from strategy.base_strategy import BaseStrategy
from core.orderbook import Order
import uuid

class StatisticalArbitrage(BaseStrategy):
    """
    Pairs Trading Strategy using Cointegration.
    Monitors the spread between two highly correlated assets.
    """
    def __init__(self, risk_manager, asset_a: str, asset_b: str, z_score_threshold: float = 2.0):
        super().__init__(risk_manager)
        self.asset_a = asset_a
        self.asset_b = asset_b
        self.z_score_threshold = z_score_threshold
        
        self.history_a = []
        self.history_b = []
        self.lookback = 100

    def update_history(self, price_a: float, price_b: float):
        self.history_a.append(price_a)
        self.history_b.append(price_b)
        if len(self.history_a) > self.lookback:
            self.history_a.pop(0)
            self.history_b.pop(0)

    def calculate_z_score(self) -> float:
        if len(self.history_a) < self.lookback:
            return 0.0
        
        # Simple spread calculation: log(A) - log(B)
        spread = np.log(self.history_a) - np.log(self.history_b)
        mean_spread = np.mean(spread)
        std_spread = np.std(spread)
        
        current_spread = spread[-1]
        z_score = (current_spread - mean_spread) / std_spread if std_spread > 0 else 0
        return z_score

    def on_market_update(self, orderbook_a, orderbook_b, current_time):
        price_a = orderbook_a.get_mid_price()
        price_b = orderbook_b.get_mid_price()
        
        if price_a == 0 or price_b == 0:
            return []

        self.update_history(price_a, price_b)
        z_score = self.calculate_z_score()
        
        orders = []
        # If z-score > threshold, spread is too high: sell A, buy B
        if z_score > self.z_score_threshold:
            if self.risk_manager.check_order_allowed('sell', 1.0):
                orders.append(Order(str(uuid.uuid4()), 'sell', price_a, 1.0, current_time))
            # Buy B logic would go here
                
        # If z-score < -threshold, spread is too low: buy A, sell B
        elif z_score < -self.z_score_threshold:
            if self.risk_manager.check_order_allowed('buy', 1.0):
                orders.append(Order(str(uuid.uuid4()), 'buy', price_a, 1.0, current_time))
                
        return orders
