# Hinglish: Yahan hum PyTorch ka use karke apna Neural Network (classifier) model banate hain.

import torch.nn as nn
import torch.nn.functional as F
from crypto_finder.ml.features import FEATURE_VECTOR_SIZE

class CryptoClassifierMLP(nn.Module):
    """
    Ek simple Multi-Layer Perceptron (MLP) model jo functions ko classify karta hai.
    """
    
    def __init__(self, input_size: int = FEATURE_VECTOR_SIZE, hidden_size: int = 128, num_classes: int = 2):
        """
        Model ki layers (hisso) ko define karta hai.
        """
        super(CryptoClassifierMLP, self).__init__()
        
        # Layers define karo
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size // 2)
        self.output_layer = nn.Linear(hidden_size // 2, num_classes)
        
        # Dropout layer (overfitting kam karne ke liye)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        """
        Forward pass: Data model ke through kaise process hoga.
        """
        # Har layer ke baad ek activation function (ReLU) apply karo
        x = F.relu(self.layer1(x))
        x = self.dropout(x)
        x = F.relu(self.layer2(x))
        x = self.dropout(x)
        
        # Final output layer (yahan activation nahi, kyunki CrossEntropyLoss use karenge)
        x = self.output_layer(x)
        return x