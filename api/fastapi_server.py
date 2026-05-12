from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(
    title="HFT Management API",
    description="High-performance control plane for the Market Making Algorithm.",
    version="2.0.0"
)

# Shared memory/state for the trading engine
engine_state = {
    "status": "RUNNING",
    "inventory": {"BTC": 1.5, "USD": 50000.0},
    "realized_pnl": 1250.50,
    "uptime_seconds": 0
}
start_time = time.time()

class RiskLimitUpdate(BaseModel):
    max_position: float
    max_drawdown: float

@app.get("/api/v1/status")
async def get_status():
    """Returns real-time status of the trading engine."""
    engine_state["uptime_seconds"] = int(time.time() - start_time)
    return engine_state

@app.post("/api/v1/risk")
async def update_risk_limits(limits: RiskLimitUpdate):
    """Dynamically update risk limits without restarting the engine."""
    if limits.max_drawdown <= 0:
        raise HTTPException(status_code=400, detail="Drawdown must be positive.")
    return {"message": "Risk limits updated successfully", "new_limits": limits.dict()}

@app.post("/api/v1/kill-switch")
async def emergency_kill():
    """Immediately halts trading and cancels all active orders."""
    engine_state["status"] = "HALTED"
    return {"message": "EMERGENCY HALT EXECUTED. All orders cancelled."}
