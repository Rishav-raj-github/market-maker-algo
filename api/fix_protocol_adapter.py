import asyncio
import time
import socket
from typing import Callable, Dict

class FIXProtocolAdapter:
    """
    Simulates a Financial Information eXchange (FIX) 4.4 protocol adapter for
    ultra-low latency direct market access (DMA).
    """
    def __init__(self, host: str, port: int, sender_comp_id: str, target_comp_id: str):
        self.host = host
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.msg_seq_num = 1
        self.is_connected = False
        self.callbacks: Dict[str, Callable] = {}
        
    def _generate_header(self, msg_type: str) -> str:
        t = time.strftime('%Y%m%d-%H:%M:%S.000', time.gmtime())
        header = f"8=FIX.4.4|9=000|35={msg_type}|49={self.sender_comp_id}|56={self.target_comp_id}|34={self.msg_seq_num}|52={t}|"
        self.msg_seq_num += 1
        return header

    async def connect(self):
        """Establish TCP connection and send Logon (35=A)"""
        print(f"Connecting to FIX Gateway at {self.host}:{self.port}...")
        await asyncio.sleep(0.1) # Simulate network delay
        self.is_connected = True
        logon_msg = self._generate_header("A") + "98=0|108=30|10=000|"
        print(f"Sent Logon: {logon_msg}")
        return True

    def send_order(self, cl_ord_id: str, symbol: str, side: str, qty: float, price: float):
        """Sends a New Order Single (35=D)"""
        if not self.is_connected:
            raise ConnectionError("FIX connection is not established.")
            
        fix_side = "1" if side.lower() == "buy" else "2"
        fix_type = "2" # Limit order
        
        msg = self._generate_header("D")
        msg += f"11={cl_ord_id}|55={symbol}|54={fix_side}|60={time.strftime('%Y%m%d-%H:%M:%S.000')}|38={qty}|40={fix_type}|44={price}|10=000|"
        
        # Simulate send
        print(f"[FIX] --> {msg}")
        
    def register_callback(self, msg_type: str, callback: Callable):
        self.callbacks[msg_type] = callback

    async def _listen_loop(self):
        """Simulates receiving Execution Reports (35=8)"""
        while self.is_connected:
            await asyncio.sleep(1.0)
            # Simulated Execution Report
            exec_report = f"8=FIX.4.4|9=120|35=8|...|150=2|151=0|14={100}|10=000|"
            if "8" in self.callbacks:
                self.callbacks["8"](exec_report)

    def disconnect(self):
        """Sends Logout (35=5)"""
        logout_msg = self._generate_header("5") + "10=000|"
        print(f"Sent Logout: {logout_msg}")
        self.is_connected = False
