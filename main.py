from core.risk_manager import RiskManager
from strategy.avellaneda_stoikov import AvellanedaStoikov
from data.simulator import MarketDataSimulator
from backtest.engine import BacktestEngine

def main():
    print("Initializing Market Maker Algorithm Simulation...")
    
    # 1. Setup Risk Manager
    # Max inventory of 10 lots, Max drawdown of $500
    risk_manager = RiskManager(max_position=10.0, max_drawdown=500.0)
    
    # 2. Setup Strategy (Avellaneda-Stoikov)
    # gamma = risk aversion, sigma = volatility guess
    strategy = AvellanedaStoikov(risk_manager, gamma=0.1, sigma=0.05, k=1.5, order_qty=1.0)
    
    # 3. Setup Market Data Simulator
    # Starts at price 100, moderate volatility
    simulator = MarketDataSimulator(initial_price=100.0, mu=0.0, sigma=0.05)
    
    # 4. Setup and run Backtest Engine
    # Run for 5000 simulation steps
    engine = BacktestEngine(strategy, simulator, risk_manager, steps=5000)
    
    print("Running Backtest Engine...")
    results = engine.run()
    
    print("\n--- Institutional Performance Report ---")
    for key, val in results.items():
        if "Ratio" in key:
            print(f"{key}: {val:.2f}")
        else:
            print(f"{key}: ${val:.2f}")
            
    print("----------------------------------------")

if __name__ == "__main__":
    main()
