from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from .database import write_inference, read_history
from .inference import predict
from .auth import require_bearer_token

app = FastAPI(title="SBDT Integrated Inference API", version="1.0.0")

class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

@app.get("/health")
def health():
    return {"status": "ok", "service": "sbdt-backend"}

@app.post("/predict")
def run_prediction(payload: PredictionRequest, token: str = Depends(require_bearer_token)):
    features = [payload.sepal_length, payload.sepal_width, payload.petal_length, payload.petal_width]
    predicted_class = predict(features)
    try:
        saved = write_inference(payload.model_dump(), predicted_class)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not save to Primary: {exc}")
    return {"prediction": predicted_class, "database_write": "primary", "record": saved}

@app.get("/history")
def history(limit: int = 20, token: str = Depends(require_bearer_token)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    try:
        records = read_history(limit)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not read from Replica: {exc}")
    return {"database_read": "replica", "count": len(records), "items": records}
