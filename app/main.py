from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Constants for salary calculation
BASE_SALARY = 30000  # Base salary
INCREMENT = 2000  # Increase per year of experience

def transform_input(years_of_experience: int) -> int:
    """Ensures that experience is non-negative."""
    return max(0, years_of_experience)

class WageRequest(BaseModel):
    years_of_experience: int

class WageResponse(BaseModel):
    predicted_wage: int

@app.post("/predict_wage", response_model=WageResponse)
def predict_wage(request: WageRequest):
    """API endpoint to predict wages based on years of experience."""
    transformed_experience = transform_input(request.years_of_experience)
    predicted_wage = BASE_SALARY + (transformed_experience * INCREMENT)
    return WageResponse(predicted_wage=predicted_wage)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
