from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request_body import CustomerChurnInput
from app.inference.predict import ChurnPredictor

router = APIRouter()

predictor_instance = ChurnPredictor()

def get_predictor():
    return predictor_instance

@router.post("/predict", response_model=dict)
def predict_customer_churn(
    input_data: CustomerChurnInput, 
    predictor: ChurnPredictor = Depends(get_predictor)
):
    
    try:
        result = predictor.predict(input_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during machine learning inference: {str(e)}"
        )