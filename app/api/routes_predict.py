
from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from app.core.dependencies import get_current_user,get_api_key
from app.services.model_service import predict_car_price


router = APIRouter()

class CarFeatures(BaseModel):
    company: str
    year : int
    owners: str
    fuel : str
    seller_type : str
    transmission : str
    km_driven : int
    mileage_mpg : float
    engine_cc : float
    max_power_bhp : float
    torque_nm : float
    seats : float

@router.post("/predict")
def predict_price(features: CarFeatures, user: str = Depends(get_current_user),_=Depends(get_api_key)):
    predictions = predict_car_price(features.model_dump())
    return {"predicted_price": predictions}

