# System Architecture

## Core Engine
The core engine is built to be synchronous and single-threaded for the critical path (order matching and risk checks) to avoid context-switching overhead.
It utilizes pre-allocated arrays and object pooling for `Order` instances to minimize garbage collection latency spikes.

## API Layer
The system supports dual operation modes:
1. **Direct Market Access (DMA)**: via the `FIXProtocolAdapter` for ultra-low latency traditional exchanges.
2. **REST/WS**: via `BinanceAdapter` and `WebSocketStreamManager` for crypto.

## Strategies
We implement modular base strategies. The flagship is the `AdvancedMarketMaker` which uses the Avellaneda-Stoikov pricing formula combined with real-time Order Flow Imbalance (OFI) calculations to dynamically adjust spreads.
