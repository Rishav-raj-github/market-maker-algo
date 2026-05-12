import random
import math
from core.orderbook import Order

class MarketDataSimulator:
    """
    Generates synthetic tick-level market data.
    Simulates a Geometric Brownian Motion (GBM) for the mid-price.
    """
    def __init__(self, initial_price=100.0, mu=0.0, sigma=0.02, dt=1.0/25200.0): # 25200 secs in a trading day
        self.price = initial_price
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.current_time = 0.0

    def step(self):
        """
        Advances the simulation by one time step and returns LOB updates.
        """
        self.current_time += self.dt
        
        # GBM step
        dw = random.gauss(0, math.sqrt(self.dt))
        dp = self.price * (self.mu * self.dt + self.sigma * dw)
        self.price += dp
        
        # Simulate LOB around the mid price (simplified)
        spread = 0.05
        best_bid = round(self.price - spread / 2.0, 2)
        best_ask = round(self.price + spread / 2.0, 2)
        
        # Return synthetic orders to populate the book
        import uuid
        bid_order = Order(str(uuid.uuid4()), 'buy', best_bid, 100.0, self.current_time)
        ask_order = Order(str(uuid.uuid4()), 'sell', best_ask, 100.0, self.current_time)
        
        return [bid_order, ask_order]
