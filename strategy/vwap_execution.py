from strategy.base_strategy import BaseStrategy
from core.orderbook import Order
import uuid

class VWAPExecution(BaseStrategy):
    """
    Volume Weighted Average Price (VWAP) execution algorithm.
    Splits a large parent order into smaller child orders based on historical volume profiles.
    """
    def __init__(self, risk_manager, total_qty: float, start_time: float, end_time: float, volume_profile: list):
        super().__init__(risk_manager)
        self.total_qty = total_qty
        self.executed_qty = 0.0
        self.start_time = start_time
        self.end_time = end_time
        self.volume_profile = volume_profile # List of expected volume percentages per interval
        self.interval_idx = 0

    def get_target_qty(self, current_time: float) -> float:
        if current_time >= self.end_time:
            return self.total_qty
            
        progress = (current_time - self.start_time) / (self.end_time - self.start_time)
        idx = min(int(progress * len(self.volume_profile)), len(self.volume_profile) - 1)
        
        cumulative_vol = sum(self.volume_profile[:idx+1])
        target = self.total_qty * cumulative_vol
        return target

    def on_market_update(self, orderbook, current_time):
        if self.executed_qty >= self.total_qty:
            return []
            
        target_qty = self.get_target_qty(current_time)
        qty_to_trade = target_qty - self.executed_qty
        
        if qty_to_trade > 0:
            price = orderbook.get_best_ask() # Aggressive execution (buying)
            if price < float('inf'):
                order = Order(str(uuid.uuid4()), 'buy', price, qty_to_trade, current_time)
                self.executed_qty += qty_to_trade
                return [order]
                
        return []
