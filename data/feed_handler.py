class FeedHandler:
    """
    Normalizes different exchange data streams into a standard internal format.
    """
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def process_binance_message(self, msg: dict):
        """Converts Binance depth update into internal standard."""
        if msg.get('e') == 'depthUpdate':
            symbol = msg.get('s')
            bids = msg.get('b', [])
            asks = msg.get('a', [])
            
            normalized = {
                'exchange': 'binance',
                'symbol': symbol,
                'bids': [(float(p), float(q)) for p, q in bids],
                'asks': [(float(p), float(q)) for p, q in asks]
            }
            self._dispatch(normalized)

    def process_fix_message(self, msg: str):
        """Converts FIX message into internal standard."""
        # Simple mock parser
        normalized = {
            'exchange': 'fix_gateway',
            'symbol': 'AAPL',
            'bids': [(150.0, 100)],
            'asks': [(150.5, 100)]
        }
        self._dispatch(normalized)

    def _dispatch(self, data: dict):
        for sub in self.subscribers:
            sub(data)
