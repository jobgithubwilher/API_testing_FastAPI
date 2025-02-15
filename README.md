# FastAPI Wage Prediction API

This is a simple FastAPI-based microservice that predicts wages based on years of experience using a basic formula.

## 1. Prepare local environment

Create a virtual env (my suggestion is Conda Environment)

```
conda create --name test_fast_api python=3.9
```

Activate the conda environment

```
conda activate test_fast_api
```

Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the application**

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API

Use a tool like `curl` or Postman to test:

```
curl -X 'POST' 'http://127.0.0.1:8000/predict_wage' \
     -H 'Content-Type: application/json' \
     -d '{"years_of_experience": 5}'
```

### 4. Run Tests

By default, when pytest runs, it doesn't automatically consider the project's root directory as part of the module search path. This can cause `ModuleNotFoundError: No module named 'app'`.

```
PYTHONPATH=. pytest
```
