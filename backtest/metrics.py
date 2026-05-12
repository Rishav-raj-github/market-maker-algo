import numpy as np

class MetricsCalculator:
    """
    Calculates institutional performance metrics for the strategy.
    """
    def __init__(self):
        self.pnl_history = []
        self.times = []
        
    def record_pnl(self, time: float, pnl: float):
        self.times.append(time)
        self.pnl_history.append(pnl)
        
    def calculate_sharpe_ratio(self, risk_free_rate=0.0) -> float:
        if len(self.pnl_history) < 2:
            return 0.0
            
        returns = np.diff(self.pnl_history)
        if len(returns) == 0 or np.std(returns) == 0:
            return 0.0
            
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        # Annualized assuming 252 trading days and returns are per step
        return (mean_return - risk_free_rate) / std_return * np.sqrt(252 * 25200)

    def calculate_max_drawdown(self) -> float:
        if not self.pnl_history:
            return 0.0
        peak = self.pnl_history[0]
        max_dd = 0.0
        for pnl in self.pnl_history:
            if pnl > peak:
                peak = pnl
            dd = peak - pnl
            if dd > max_dd:
                max_dd = dd
        return max_dd

    def get_summary(self):
        return {
            "Total PnL": self.pnl_history[-1] if self.pnl_history else 0.0,
            "Sharpe Ratio": self.calculate_sharpe_ratio(),
            "Max Drawdown": self.calculate_max_drawdown()
        }
