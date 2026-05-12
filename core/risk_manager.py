class RiskManager:
    """
    Manages inventory risk and enforces position limits for the market maker.
    """
    def __init__(self, max_position: float, max_drawdown: float):
        self.max_position = max_position
        self.max_drawdown = max_drawdown
        
        self.current_position = 0.0
        self.peak_pnl = 0.0
        self.current_pnl = 0.0
        
    def check_order_allowed(self, side: str, qty: float) -> bool:
        """
        Checks if an order is allowed based on current inventory limits.
        """
        if side == 'buy':
            if self.current_position + qty > self.max_position:
                return False
        elif side == 'sell':
            if self.current_position - qty < -self.max_position:
                return False
        return True
        
    def update_position(self, side: str, qty: float, price: float):
        """
        Updates internal inventory based on an execution.
        """
        if side == 'buy':
            self.current_position += qty
        else:
            self.current_position -= qty

    def update_pnl(self, realized_pnl: float, unrealized_pnl: float):
        self.current_pnl = realized_pnl + unrealized_pnl
        if self.current_pnl > self.peak_pnl:
            self.peak_pnl = self.current_pnl
            
    def is_drawdown_exceeded(self) -> bool:
        drawdown = self.peak_pnl - self.current_pnl
        return drawdown >= self.max_drawdown
