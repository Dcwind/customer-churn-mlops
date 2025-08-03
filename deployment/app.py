import mlflow
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


# Pydantic Model for Input Validation
# This ensures that any data sent to /predict endpoint
# has the correct structure and data types.
class CustomerData(BaseModel):
    tenure: float
    monthlycharges: float
    totalcharges: float


# FastAPI App Initialization
app = FastAPI()

# Load the Model from MLflow Model Registry
# For the MVP, I'm loading the latest version of the model.
# In a production system, I would load a specific stage like "Production".
MODEL_NAME = "churn-prediction-mvp-lr"
model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")


# Prediction Endpoint
@app.post("/predict")
def predict(data: CustomerData):
    """
    Receives customer data, makes a prediction using the loaded model,
    and returns the churn prediction.
    """
    # Convert the incoming Pydantic object to a pandas DataFrame
    # because scikit-learn model expects it in this format.
    input_df = pd.DataFrame([data.dict()])

    # Get the prediction from the model
    prediction = model.predict(input_df)[0]

    # Return the prediction in a JSON response
    return {"churn_prediction": int(prediction)}


# Health Check Endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
