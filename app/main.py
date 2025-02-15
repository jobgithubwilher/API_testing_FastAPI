import os

import yaml
from fastapi import FastAPI

from app.models import WageRequest, WageResponse

app = FastAPI()


# Load configuration from YAML file dynamically
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../config.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


config = load_config()
BASE_SALARY = config["BASE_SALARY"]  # Base salary
INCREMENT = config["INCREMENT"]  # Increase per year of experience


def transform_input(years_of_experience: int) -> int:
    """Ensures that experience is non-negative."""
    return max(0, years_of_experience)


@app.post("/predict_wage", response_model=WageResponse)
def predict_wage(request: WageRequest):
    """API endpoint to predict wages based on years of experience.

    Parameters:
        request (WageRequest): Contains the years of experience.

    Returns:
        WageResponse: Contains the predicted wage.
    """
    transformed_experience = transform_input(request.years_of_experience)
    predicted_wage = BASE_SALARY + (transformed_experience * INCREMENT)
    return WageResponse(predicted_wage=predicted_wage)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
