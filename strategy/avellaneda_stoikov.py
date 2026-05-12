from strategy.base_strategy import BaseStrategy
import math
import uuid
from core.orderbook import Order

class AvellanedaStoikov(BaseStrategy):
    """
    Implementation of the Avellaneda-Stoikov market making model.
    Adjusts the reservation price and optimal spread based on inventory.
    """
    def __init__(self, risk_manager, gamma=0.1, sigma=1.0, k=1.5, order_qty=1.0):
        super().__init__(risk_manager)
        self.gamma = gamma      # Risk aversion parameter
        self.sigma = sigma      # Market volatility
        self.k = k              # Liquidity parameter
        self.order_qty = order_qty
        self.current_time = 0.0
        self.terminal_time = 1.0 # T, normalized to 1 day

    def calculate_reservation_price(self, mid_price: float, time_left: float, inventory: float) -> float:
        """
        Calculates the optimal reservation price based on current inventory.
        r(s, t) = s - q * gamma * sigma^2 * (T - t)
        """
        return mid_price - inventory * self.gamma * (self.sigma ** 2) * time_left

    def calculate_optimal_spread(self, time_left: float) -> float:
        """
        Calculates the optimal bid-ask spread.
        spread = gamma * sigma^2 * (T - t) + (2/gamma) * ln(1 + gamma / k)
        """
        return self.gamma * (self.sigma ** 2) * time_left + (2 / self.gamma) * math.log(1 + self.gamma / self.k)

    def generate_quotes(self, orderbook, current_time) -> tuple:
        """
        Returns (bid_price, ask_price) based on A-S model.
        """
        mid_price = orderbook.get_mid_price()
        if mid_price == 0:
            return None, None
            
        time_left = max(0, self.terminal_time - current_time)
        inventory = self.risk_manager.current_position
        
        res_price = self.calculate_reservation_price(mid_price, time_left, inventory)
        spread = self.calculate_optimal_spread(time_left)
        
        optimal_bid = res_price - spread / 2.0
        optimal_ask = res_price + spread / 2.0
        
        # Round to 2 decimal places (standard tick size)
        return round(optimal_bid, 2), round(optimal_ask, 2)

    def on_market_update(self, orderbook, current_time):
        """
        Generates new quotes based on the updated market data and inventory.
        Returns a list of Order objects to be placed.
        """
        self.current_time = current_time
        bid_px, ask_px = self.generate_quotes(orderbook, current_time)
        
        new_orders = []
        if bid_px is not None and self.risk_manager.check_order_allowed('buy', self.order_qty):
            new_orders.append(Order(str(uuid.uuid4()), 'buy', bid_px, self.order_qty, current_time))
            
        if ask_px is not None and self.risk_manager.check_order_allowed('sell', self.order_qty):
            new_orders.append(Order(str(uuid.uuid4()), 'sell', ask_px, self.order_qty, current_time))
            
        return new_orders
