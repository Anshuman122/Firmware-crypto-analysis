# Hinglish: API ka main entry point. Hum yahan apne endpoints router ko include kar rahe hain.

from fastapi import FastAPI
from crypto_finder.api import endpoints

# FastAPI app ka object banao
app = FastAPI(
    title="Crypto Finder API",
    description="Firmware binaries me cryptographic primitives dhundhne ke liye API.",
    version="0.1.0"
)

# Endpoints router ko main app me include karo
app.include_router(endpoints.router, prefix="/api/v1", tags=["Analysis"])

@app.get("/", tags=["General"])
def read_root():
    """API ka welcome message."""
    return {"message": "Welcome to Crypto Finder API! API documentation ke liye /docs par jayein."}