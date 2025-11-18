import torch
import torch.nn as nn

class MutationNet(nn.Module):
    """Simple CNN + BiLSTM network for sequence classification."""

    def __init__(self, num_classes: int = 2):
        super().__init__()

        # Input: (batch, 4, seq_len) for one-hot A/C/G/T
        self.conv = nn.Sequential(
            nn.Conv1d(4, 32, kernel_size=7, padding=3),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool1d(2),
        )

        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=128,
            batch_first=True,
            bidirectional=True,
        )

        self.fc = nn.Sequential(
            nn.Linear(128 * 2, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        # x: (batch, 4, seq_len)
        x = self.conv(x)
        # x: (batch, channels, seq_len_reduced)
        x = x.permute(0, 2, 1)  # (batch, seq_len_reduced, channels)

        _, (h, _) = self.lstm(x)
        # h: (num_directions, batch, hidden_size)
        h_cat = torch.cat((h[0], h[1]), dim=1)  # (batch, 2 * hidden_size)

        logits = self.fc(h_cat)
        return logits
