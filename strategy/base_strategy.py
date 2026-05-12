import math

class BaseStrategy:
    """
    Abstract base class for quantitative market making strategies.
    """
    def __init__(self, risk_manager):
        self.risk_manager = risk_manager
        self.active_orders = {}

    def on_market_update(self, orderbook):
        """
        Called when the LOB updates. To be implemented by subclasses.
        """
        raise NotImplementedError

    def on_trade_execution(self, execution):
        """
        Called when one of the strategy's orders is executed.
        """
        raise NotImplementedError
