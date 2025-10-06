# Hinglish: Yeh file lifter se mile data ko ek numerical vector (features) me convert karti hai,
# jise hamara ML model samajh sake.

import numpy as np
from typing import Dict, Any, List

# Ek simple vocabulary (aap isse aur bada kar sakte hain)
# Yeh P-Code operations ko numbers me map karta hai.
PCODE_VOCAB = {
    "COPY": 1, "LOAD": 2, "STORE": 3,
    "BRANCH": 4, "CBRANCH": 5, "BRANCHIND": 6,
    "CALL": 7, "CALLIND": 8, "RETURN": 9,
    "INT_EQUAL": 10, "INT_NOTEQUAL": 11,
    "INT_SLESS": 12, "INT_SLESSEQUAL": 13, "INT_LESS": 14, "INT_LESSEQUAL": 15,
    "INT_ZEXT": 16, "INT_SEXT": 17,
    "INT_ADD": 18, "INT_SUB": 19, "INT_CARRY": 20, "INT_SCARRY": 21,
    "INT_AND": 22, "INT_OR": 23, "INT_XOR": 24,
    "INT_MULT": 25, "INT_DIV": 26, "INT_SDIV": 27, "INT_REM": 28, "INT_SREM": 29,
    "INT_LEFT": 30, "INT_RIGHT": 31, "INT_SRIGHT": 32,
    "BOOL_NEGATE": 33, "BOOL_XOR": 34, "BOOL_AND": 35, "BOOL_OR": 36,
    "FLOAT_ADD": 37, "FLOAT_SUB": 38, "FLOAT_MULT": 39, "FLOAT_DIV": 40,
    "CAST": 41, "CPOOLREF": 42, "NEW": 43,
    "UNK": 99 # Unknown operations
}
FEATURE_VECTOR_SIZE = len(PCODE_VOCAB) + 2  # P-Code counts + size + instruction_count

def extract_features_from_function(func_data: Dict[str, Any]) -> np.ndarray:
    """
    Ek single function ke data se feature vector extract karta hai.
    """
    # Feature vector ko zero se initialize karo.
    features = np.zeros(FEATURE_VECTOR_SIZE, dtype=np.float32)

    # Feature 1 & 2: Basic metadata (normalized)
    features[0] = np.log1p(func_data.get("size", 0))  # Log transform for stability
    features[1] = np.log1p(func_data.get("instruction_count", 0))
    
    # Feature 3+: P-Code operation counts
    pcode_ops = func_data.get("pcode", [])
    for op_str in pcode_ops:
        op_name = op_str.split(" ")[0]
        op_id = PCODE_VOCAB.get(op_name, PCODE_VOCAB["UNK"])
        
        # Vocabulary me har op_id ek unique index hai.
        # Hum us index ko use karke vector me count badha rahe hain.
        if (op_id + 1) < FEATURE_VECTOR_SIZE: # Index 0 aur 1 reserved hain
            features[op_id + 1] += 1
            
    # Vector ko normalize karo (sum of counts = 1) for P-Code features
    pcode_sum = np.sum(features[2:])
    if pcode_sum > 0:
        features[2:] /= pcode_sum

    return features