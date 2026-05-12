from core.orderbook import Order, OrderBook
import uuid

class MatchingEngine:
    """
    Simulates a financial exchange matching engine.
    Matches incoming market orders against the limit order book.
    """
    def __init__(self, orderbook: OrderBook):
        self.orderbook = orderbook
        self.trades = []

    def process_market_order(self, side: str, qty: float) -> list:
        """
        Executes a market order against the LOB and returns execution reports.
        """
        side = side.lower()
        remaining_qty = qty
        executions = []
        
        book = self.orderbook.asks if side == 'buy' else self.orderbook.bids
        # Sort prices: ascending for asks (we buy at lowest ask), descending for bids (we sell at highest bid)
        reverse_sort = True if side == 'sell' else False
        
        prices = sorted(book.keys(), reverse=reverse_sort)
        
        for price in prices:
            if remaining_qty <= 0:
                break
                
            orders_at_price = list(book[price].values())
            for order in orders_at_price:
                if remaining_qty <= 0:
                    break
                    
                exec_qty = min(remaining_qty, order.qty)
                order.qty -= exec_qty
                remaining_qty -= exec_qty
                
                executions.append({
                    'trade_id': str(uuid.uuid4()),
                    'price': price,
                    'qty': exec_qty,
                    'maker_order_id': order.order_id,
                    'side': side
                })
                
                if order.qty <= 0:
                    self.orderbook.cancel_order(order.order_id)
                    
        self.trades.extend(executions)
        return executions
