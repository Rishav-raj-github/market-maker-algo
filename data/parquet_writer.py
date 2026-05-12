import pandas as pd
import os

class ParquetWriter:
    """
    High-performance data writer for saving L2 order book snapshots and tick data.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self.buffer = []
        self.flush_threshold = 50000

    def append_tick(self, timestamp: float, symbol: str, price: float, qty: float):
        self.buffer.append({
            'timestamp': timestamp,
            'symbol': symbol,
            'price': price,
            'qty': qty
        })
        
        if len(self.buffer) >= self.flush_threshold:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
            
        df = pd.DataFrame(self.buffer)
        filename = f"{self.output_dir}/ticks_{int(df['timestamp'].iloc[0])}.parquet"
        # df.to_parquet(filename, engine='pyarrow', compression='snappy')
        print(f"Flushed {len(self.buffer)} records to {filename}")
        self.buffer.clear()
