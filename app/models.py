from pydantic import BaseModel


class WageRequest(BaseModel):
    years_of_experience: int


class WageResponse(BaseModel):
    predicted_wage: int
