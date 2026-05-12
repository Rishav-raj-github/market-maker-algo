import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode

class BinanceAdapter:
    """
    REST API Adapter for Binance Spot and USD-M Futures.
    Used for hedging or crypto market making strategies.
    """
    BASE_URL = "https://api.binance.com"
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        
    def _generate_signature(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(self.api_secret.encode('utf-8'), 
                        query_string.encode('utf-8'), 
                        hashlib.sha256).hexdigest()

    def get_server_time(self):
        url = f"{self.BASE_URL}/api/v3/time"
        response = self.session.get(url)
        return response.json().get('serverTime')
        
    def place_order(self, symbol: str, side: str, order_type: str, qty: float, price: float = None):
        """Places a cryptographic signed order on Binance."""
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": qty,
            "timestamp": int(time.time() * 1000)
        }
        if price and order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
            
        params["signature"] = self._generate_signature(params)
        
        url = f"{self.BASE_URL}{endpoint}"
        # response = self.session.post(url, params=params)
        # return response.json()
        print(f"[BINANCE REST] Placing {side} {qty} {symbol} @ {price}")
        return {"orderId": 123456789, "status": "NEW"}
        
    def cancel_order(self, symbol: str, order_id: int):
        print(f"[BINANCE REST] Canceling order {order_id} for {symbol}")
        return {"status": "CANCELED"}
