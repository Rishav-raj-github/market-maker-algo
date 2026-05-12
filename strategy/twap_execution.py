from strategy.base_strategy import BaseStrategy
from core.orderbook import Order
import uuid

class TWAPExecution(BaseStrategy):
    """
    Time Weighted Average Price (TWAP) execution algorithm.
    Executes trades at regular time intervals to minimize market impact.
    """
    def __init__(self, risk_manager, total_qty: float, num_intervals: int, interval_seconds: float):
        super().__init__(risk_manager)
        self.total_qty = total_qty
        self.num_intervals = num_intervals
        self.interval_seconds = interval_seconds
        
        self.qty_per_interval = total_qty / num_intervals
        self.intervals_completed = 0
        self.last_exec_time = 0.0

    def on_market_update(self, orderbook, current_time):
        if self.intervals_completed >= self.num_intervals:
            return []
            
        if current_time - self.last_exec_time >= self.interval_seconds:
            price = orderbook.get_best_ask()
            if price < float('inf'):
                order = Order(str(uuid.uuid4()), 'buy', price, self.qty_per_interval, current_time)
                self.last_exec_time = current_time
                self.intervals_completed += 1
                return [order]
                
        return []
