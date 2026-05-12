from core.orderbook import OrderBook
from core.matching_engine import MatchingEngine
from data.simulator import MarketDataSimulator
from backtest.metrics import MetricsCalculator
import random

class BacktestEngine:
    """
    Event-driven backtesting engine for the market making strategy.
    """
    def __init__(self, strategy, simulator: MarketDataSimulator, risk_manager, steps: int = 1000):
        self.strategy = strategy
        self.simulator = simulator
        self.risk_manager = risk_manager
        self.steps = steps
        
        self.orderbook = OrderBook()
        self.matching_engine = MatchingEngine(self.orderbook)
        self.metrics = MetricsCalculator()
        
    def run(self):
        for step in range(self.steps):
            # 1. Market Data Update
            market_orders = self.simulator.step()
            for o in market_orders:
                self.orderbook.add_order(o)
                
            # 2. Strategy generates quotes based on updated book
            strategy_orders = self.strategy.on_market_update(self.orderbook, self.simulator.current_time)
            
            # Remove old strategy orders for simplicity in this demo and place new ones
            for old_o_id in list(self.strategy.active_orders.keys()):
                self.orderbook.cancel_order(old_o_id)
            self.strategy.active_orders.clear()
            
            for so in strategy_orders:
                self.strategy.active_orders[so.order_id] = so
                self.orderbook.add_order(so)
                
            # 3. Simulate external retail flow matching against our quotes
            # We randomly simulate a market buy or sell to hit our quotes
            if random.random() < 0.1: # 10% chance of an external market order
                side = 'buy' if random.random() < 0.5 else 'sell'
                qty = 1.0 # 1 lot
                executions = self.matching_engine.process_market_order(side, qty)
                
                # 4. Process Executions and update risk manager
                for exec in executions:
                    if exec['maker_order_id'] in self.strategy.active_orders:
                        # We got filled!
                        fill_side = 'sell' if side == 'buy' else 'buy'
                        fill_price = exec['price']
                        fill_qty = exec['qty']
                        
                        self.risk_manager.update_position(fill_side, fill_qty, fill_price)
                        # Simplified PnL: assuming we buy at bid, sell at ask. 
                        # A proper implementation tracks average entry price.
                        if fill_side == 'sell':
                            # We sold, meaning realized PnL depends on previous buys. 
                            # Simplification for demo: Arbitrary small profit per fill.
                            self.risk_manager.update_pnl(0.05 * fill_qty, 0) 
                            
            # Record metrics
            self.metrics.record_pnl(self.simulator.current_time, self.risk_manager.current_pnl)
            
        print("Backtest Complete.")
        return self.metrics.get_summary()
