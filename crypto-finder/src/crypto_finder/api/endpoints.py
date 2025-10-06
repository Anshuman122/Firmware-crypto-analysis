# Hinglish: API ka main logic yahan hai. Humne endpoints ko ek 'router' me organize kiya hai.

from fastapi import APIRouter, HTTPException
import torch
import torch.nn.functional as F
import numpy as np

from crypto_finder.api.models import FunctionAnalysisRequest, AnalysisResponse, Prediction
from crypto_finder.ml.models import CryptoClassifierMLP
from crypto_finder.ml.features import extract_features_from_function
from crypto_finder.common.config import settings
from crypto_finder.common.logging import log

router = APIRouter()

# Trained model ko load karo
MODEL_PATH = settings.models_dir / "crypto_classifier.pth"
model = CryptoClassifierMLP()
if not MODEL_PATH.exists():
    log.warning("Model file nahi mili. API dummy responses degi.")
    model = None
else:
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval() # Model ko evaluation mode me set karo
    log.success(f"ML model '{MODEL_PATH.name}' successfully load ho gaya.")


@router.post("/predict", response_model=AnalysisResponse)
def predict_function(request: FunctionAnalysisRequest):
    """
    Ek function ke lifted data par crypto prediction run karta hai.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not available. Please train the model first.")

    log.info(f"Function '{request.name}' ke liye prediction request aayi.")
    
    # Request data ko dictionary me convert karo
    func_data = request.model_dump()
    
    # Features extract karo
    features = extract_features_from_function(func_data)
    feature_tensor = torch.from_numpy(features).unsqueeze(0) # Batch dimension add karo
    
    with torch.no_grad(): # Gradient calculation ko disable karo for faster inference
        outputs = model(feature_tensor)
        # Softmax ka use karke probabilities (confidence) nikalo
        probabilities = F.softmax(outputs, dim=1)[0]
        predicted_idx = torch.argmax(probabilities).item()

    label = "crypto" if predicted_idx == 1 else "non-crypto"
    confidence = probabilities[predicted_idx].item()

    log.info(f"Prediction: {label} (Confidence: {confidence:.2f})")
    
    return AnalysisResponse(
        function_name=request.name,
        prediction=Prediction(label=label, confidence=confidence)
    )