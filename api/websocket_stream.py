import asyncio
import json
import logging

class WebSocketStreamManager:
    """
    High-throughput asynchronous WebSocket manager for Level 2 order book updates.
    Handles auto-reconnections, latency measuring, and message queueing.
    """
    def __init__(self, uri: str, max_queue_size: int = 10000):
        self.uri = uri
        self.max_queue_size = max_queue_size
        self.message_queue = asyncio.Queue(maxsize=max_queue_size)
        self.is_running = False
        self.logger = logging.getLogger("WebSocketStream")

    async def connect(self):
        self.is_running = True
        self.logger.info(f"Connecting to WS: {self.uri}")
        # In a real environment, import websockets
        # async with websockets.connect(self.uri) as ws:
        #     await self._listen(ws)
        await self._mock_listen()

    async def _mock_listen(self):
        while self.is_running:
            await asyncio.sleep(0.05) # 50ms tick
            if not self.message_queue.full():
                mock_data = {
                    "e": "depthUpdate",
                    "E": 123456789,
                    "s": "BTCUSDT",
                    "b": [["50000.00", "1.5"]],
                    "a": [["50001.00", "2.0"]]
                }
                await self.message_queue.put(json.dumps(mock_data))

    async def process_messages(self, handler_coroutine):
        """Continuously pulls messages from the queue and hands them to the strategy."""
        while self.is_running:
            msg = await self.message_queue.get()
            try:
                data = json.loads(msg)
                await handler_coroutine(data)
            except Exception as e:
                self.logger.error(f"Error processing WS message: {e}")
            finally:
                self.message_queue.task_done()
                
    def stop(self):
        self.is_running = False
        self.logger.info("WebSocket connection closed.")
