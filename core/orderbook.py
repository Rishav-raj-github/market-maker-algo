import collections
import time
from typing import Dict, List, Optional, Tuple

class Order:
    """Represents a single limit order in the market."""
    def __init__(self, order_id: str, side: str, price: float, qty: float, timestamp: Optional[float] = None):
        self.order_id = order_id
        self.side = side.lower()
        self.price = price
        self.qty = qty
        self.timestamp = timestamp or time.time()

class OrderBook:
    """A Level 2 Limit Order Book (LOB) tracking bids and asks."""
    def __init__(self):
        self.bids: Dict[float, collections.OrderedDict] = collections.defaultdict(collections.OrderedDict)
        self.asks: Dict[float, collections.OrderedDict] = collections.defaultdict(collections.OrderedDict)
        self.orders: Dict[str, Order] = {}

    def add_order(self, order: Order):
        self.orders[order.order_id] = order
        if order.side == 'buy':
            self.bids[order.price][order.order_id] = order
        else:
            self.asks[order.price][order.order_id] = order

    def cancel_order(self, order_id: str):
        if order_id not in self.orders:
            return
        order = self.orders.pop(order_id)
        book = self.bids if order.side == 'buy' else self.asks
        if order.price in book and order_id in book[order.price]:
            del book[order.price][order_id]
            if not book[order.price]:
                del book[order.price]

    def get_best_bid(self) -> float:
        return max(self.bids.keys()) if self.bids else 0.0

    def get_best_ask(self) -> float:
        return min(self.asks.keys()) if self.asks else float('inf')

    def get_mid_price(self) -> float:
        bb = self.get_best_bid()
        ba = self.get_best_ask()
        if bb > 0 and ba < float('inf'):
            return (bb + ba) / 2.0
        return bb if bb > 0 else (ba if ba < float('inf') else 0.0)

    def get_spread(self) -> float:
        return self.get_best_ask() - self.get_best_bid()
