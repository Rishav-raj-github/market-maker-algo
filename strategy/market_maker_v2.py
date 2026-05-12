from strategy.avellaneda_stoikov import AvellanedaStoikov
from core.orderbook import Order
import uuid

class AdvancedMarketMaker(AvellanedaStoikov):
    """
    Advanced Market Maker adding Order Flow Imbalance (OFI) and Adverse Selection protection.
    """
    def __init__(self, risk_manager, gamma=0.1, sigma=1.0, k=1.5, order_qty=1.0, ofi_threshold=0.5):
        super().__init__(risk_manager, gamma, sigma, k, order_qty)
        self.ofi_threshold = ofi_threshold
        self.last_best_bid = 0.0
        self.last_best_ask = 0.0

    def calculate_ofi(self, orderbook) -> float:
        """
        Calculates Order Flow Imbalance (OFI) to predict short-term price movements.
        Positive OFI indicates buying pressure, negative indicates selling pressure.
        """
        current_bid = orderbook.get_best_bid()
        current_ask = orderbook.get_best_ask()
        
        bid_vol = sum(o.qty for o in orderbook.bids.get(current_bid, {}).values())
        ask_vol = sum(o.qty for o in orderbook.asks.get(current_ask, {}).values())
        
        self.last_best_bid = current_bid
        self.last_best_ask = current_ask
        
        total_vol = bid_vol + ask_vol
        return (bid_vol - ask_vol) / total_vol if total_vol > 0 else 0.0

    def on_market_update(self, orderbook, current_time):
        ofi = self.calculate_ofi(orderbook)
        
        # Pull quotes if adverse selection risk is too high
        if abs(ofi) > self.ofi_threshold:
            print(f"[AMM] High toxic flow detected (OFI: {ofi:.2f}). Pulling liquidity.")
            return [] # Provide no liquidity
            
        # Otherwise, fall back to standard Avellaneda-Stoikov pricing
        return super().on_market_update(orderbook, current_time)
