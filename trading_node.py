import asyncio
import logging
from uvicorn import Config, Server

# Core Infrastructure
from api.fastapi_server import app as fastapi_app
from api.websocket_stream import WebSocketStreamManager
from core.risk_manager import RiskManager
from utils.logger import setup_logger

# Strategy & Models
from strategy.market_maker_v2 import AdvancedMarketMaker

logger = setup_logger("TradingNode", logging.INFO)

class TradingNode:
    """
    The unified AsyncIO entrypoint that stitches together FastAPI, 
    the Cython/Python Engine, WebSocket streams, and the ML Strategy.
    """
    def __init__(self):
        self.risk_manager = RiskManager(max_position=100.0, max_drawdown=5000.0)
        self.strategy = AdvancedMarketMaker(self.risk_manager)
        self.ws_manager = WebSocketStreamManager("wss://stream.binance.com:9443/ws/btcusdt@depth")
        
    async def process_market_data(self, data: dict):
        """Callback for live WebSocket data."""
        # In a real environment, this would feed into the FastMatchingEngine (Cython)
        # and the PyTorch LSTM model.
        pass

    async def run_fastapi(self):
        """Runs the FastAPI control plane in the same event loop."""
        logger.info("Starting FastAPI Control Plane on port 8000...")
        config = Config(app=fastapi_app, host="0.0.0.0", port=8000, loop="asyncio")
        server = Server(config)
        await server.serve()

    async def run_trading_loop(self):
        """Main event loop connecting feeds to strategy."""
        logger.info("Initializing WebSocket streams & Cython matching engine...")
        # Start background WS connection
        ws_task = asyncio.create_task(self.ws_manager.connect())
        
        # Start processing queue
        process_task = asyncio.create_task(self.ws_manager.process_messages(self.process_market_data))
        
        logger.info("Trading Node is now fully operational.")
        await asyncio.gather(ws_task, process_task)

    async def start(self):
        """Bootstraps the entire microservice."""
        logger.info("Bootstrapping Institutional Trading Node...")
        
        api_task = asyncio.create_task(self.run_fastapi())
        trading_task = asyncio.create_task(self.run_trading_loop())
        
        await asyncio.gather(api_task, trading_task)

if __name__ == "__main__":
    node = TradingNode()
    try:
        asyncio.run(node.start())
    except KeyboardInterrupt:
        logger.info("Trading Node shut down by user.")
