import torch
import torch.nn as nn

class LSTMPricePredictor(nn.Module):
    """
    Long Short-Term Memory (LSTM) network to predict short-term price movements 
    based on Order Book micro-structure features (e.g., L2 imbalances, trade flow).
    """
    def __init__(self, input_size=10, hidden_layer_size=64, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        
        # LSTM layer to capture temporal dependencies in tick data
        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
        
        # Fully connected layer to output the predicted price delta
        self.linear = nn.Linear(hidden_layer_size, output_size)

    def forward(self, input_seq):
        lstm_out, _ = self.lstm(input_seq)
        # Take the output of the last time step
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions

def predict_next_tick(model, current_features: torch.Tensor) -> float:
    """Inference function for the high-frequency trading engine."""
    model.eval()
    with torch.no_grad():
        prediction = model(current_features.unsqueeze(0))
    return prediction.item()
