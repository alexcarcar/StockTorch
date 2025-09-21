import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd

# 1. Dataset
class StockDataset(Dataset):
    def __init__(self, csv_file, seq_length=20):
        self.data = pd.read_csv(csv_file)
        self.seq_length = seq_length
        self.prices = self.data['Close'].values

    def __len__(self):
        return len(self.prices) - self.seq_length

    def __getitem__(self, idx):
        seq = self.prices[idx:idx+self.seq_length]
        label = self.prices[idx+self.seq_length]
        return torch.tensor(seq, dtype=torch.float32), torch.tensor(label, dtype=torch.float32)

# 2. Model
class StockLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = x.unsqueeze(-1)  # [batch, seq_length, 1]
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze()

# 3. Training loop
def train_model(csv_file):
    dataset = StockDataset(csv_file)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    model = StockLSTM()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(10):
        for seq, label in dataloader:
            optimizer.zero_grad()
            output = model(seq)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item():.4f}')

if __name__ == '__main__':
    train_model('historical_stock_data.csv')
