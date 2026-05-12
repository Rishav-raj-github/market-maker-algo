import asyncio
from trading_node import TradingNode

def main():
    """
    Unified Application Entrypoint.
    Starts the full Trading Node (FastAPI, WebSockets, Cython Engine).
    """
    print("Launching HFT-MMS Distributed Architecture...")
    node = TradingNode()
    try:
        asyncio.run(node.start())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")

if __name__ == "__main__":
    main()
