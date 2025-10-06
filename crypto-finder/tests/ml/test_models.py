# Hinglish: Hamare ML model ke liye ek basic test.
# Yeh check karta hai ki model create ho raha hai aur data process kar sakta hai ya nahi.

import torch
from crypto_finder.ml.models import CryptoClassifierMLP
from crypto_finder.ml.features import FEATURE_VECTOR_SIZE

def test_model_creation():
    """Test karta hai ki model bina error ke create ho raha hai."""
    model = CryptoClassifierMLP()
    assert model is not None

def test_model_forward_pass():
    """Test karta hai ki model ka forward pass sahi se kaam kar raha hai."""
    model = CryptoClassifierMLP()
    
    # Ek dummy input tensor banao
    # Batch size = 4, features = FEATURE_VECTOR_SIZE
    dummy_input = torch.randn(4, FEATURE_VECTOR_SIZE)
    
    # Forward pass run karo
    output = model(dummy_input)
    
    # Check karo ki output ka shape sahi hai
    # Batch size = 4, number of classes = 2
    assert output.shape == (4, 2)