import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("years_of_experience, expected_wage", [
    (5, 40000),  # Normal case
    (-2, 30000),  # Negative experience should return base salary
    (0, 30000),  # Zero experience should return base salary
    (10, 50000),  # Higher experience case
    (100, 230000)  # Extreme case
])
def test_predict_wage(years_of_experience, expected_wage):
    """Parameterized test for the API endpoint with multiple cases."""
    response = client.post("/predict_wage", json={"years_of_experience": years_of_experience})
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    assert response.json()["predicted_wage"] == expected_wage, f"Expected {expected_wage} but got {response.json()['predicted_wage']}"

@pytest.mark.parametrize("invalid_input", [
    {"years_of_experience": "five"},  # String instead of integer
    {"years_of_experience": None},  # None value
    {"years_of_experience": 5.5},  # Float value
    {},  # Missing input
    {"wrong_key": 5}  # Incorrect key
])
def test_predict_wage_invalid_input(invalid_input):
    """Test for invalid input cases."""
    response = client.post("/predict_wage", json=invalid_input)
    assert response.status_code == 422, f"Expected status 422 but got {response.status_code}"
    assert "detail" in response.json(), "Expected validation error message"

@pytest.mark.parametrize("years_of_experience", [
    5, -2, 0, 10, 100
])
def test_predict_wage_response_structure(years_of_experience):
    """Test that response structure is correct."""
    response = client.post("/predict_wage", json={"years_of_experience": years_of_experience})
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    json_response = response.json()
    assert "predicted_wage" in json_response, "Response should contain 'predicted_wage' key"
    assert isinstance(json_response["predicted_wage"], int), "Predicted wage should be an integer"

def test_predict_wage_method_not_allowed():
    """Ensure that unsupported HTTP methods return 405 Method Not Allowed."""
    response = client.get("/predict_wage")  # Using GET instead of POST
    assert response.status_code == 405, f"Expected status 405 but got {response.status_code}"
