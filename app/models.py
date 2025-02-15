from pydantic import BaseModel, conint


class WageRequest(BaseModel):
    years_of_experience: conint(gt=0)  # Must be greater than 0


class WageResponse(BaseModel):
    predicted_wage: int
