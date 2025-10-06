# Hinglish: Yeh script hamare ML model ko data par train karti hai.

import typer
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from crypto_finder.ml.datasets import CryptoFuncDataset
from crypto_finder.ml.models import CryptoClassifierMLP
from crypto_finder.common.logging import log
from crypto_finder.common.config import settings

app = typer.Typer()

@app.command()
def train(
    data_dir: Path = typer.Option(..., "--data-dir", help="Lifted JSON files wali directory."),
    annotations_file: Path = typer.Option(..., "--annotations-file", help="Labels wali CSV file."),
    epochs: int = typer.Option(20, "--epochs", help="Training epochs ka number."),
    learning_rate: float = typer.Option(0.001, "--lr", help="Optimizer ka learning rate."),
    batch_size: int = typer.Option(32, "--batch-size"),
):
    """ML model ko crypto functions pehchanne ke liye train karta hai."""
    log.info("Model training process shuru ho raha hai...")
    
    # Dataset banao
    full_dataset = CryptoFuncDataset(data_dir=data_dir, annotations_file=annotations_file)
    
    # Dataset ko train aur validation sets me split karo (80% train, 20% validation)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    # Model, loss, aur optimizer setup karo
    model = CryptoClassifierMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    log.info(f"Training shuru ho rahi hai: {epochs} epochs, batch size: {batch_size}, lr: {learning_rate}")
    
    # Training loop
    for epoch in range(epochs):
        model.train() # Model ko training mode me set karo
        for features, labels in train_loader:
            # Forward pass
            outputs = model(features)
            loss = criterion(outputs, labels)
            
            # Backward pass aur optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        log.info(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    log.success("Training complete.")
    
    # Trained model ko save karo
    model_save_path = settings.models_dir / "crypto_classifier.pth"
    torch.save(model.state_dict(), model_save_path)
    log.info(f"Model saved to: {model_save_path}")

if __name__ == "__main__":
    app()