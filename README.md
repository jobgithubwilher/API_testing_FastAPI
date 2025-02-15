# **FastAPI Wage Prediction API**

This is a **FastAPI-based microservice** that predicts wages based on years of experience using a simple model.

---

## **1️⃣ Project Setup**

### **1.1 Clone the Repository**
```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### **1.2 Create a Virtual Environment**
It is recommended to use Conda:
```bash
conda create --name test_fast_api python=3.9 -y
conda activate test_fast_api
```
Alternatively, using `venv`:
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### **1.3 Install Dependencies**
Ensure all dependencies are correctly installed:
```bash
pip install -r requirements.txt
```
If missing, regenerate it:
```bash
pip freeze > requirements.txt
```

---

## **2️⃣ Run the Application**
Start the FastAPI app with `uvicorn`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

For **Dockerized Deployment**:
```bash
docker build -t fastapi-wage-api .
docker run -p 8000:8000 fastapi-wage-api
```

Using **Docker Compose**:
```bash
docker-compose up --build
```

---

## **3️⃣ API Documentation**
FastAPI generates interactive API docs:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **4️⃣ Test the API**
Use `curl`, Postman, or Python to test:

### **cURL Request**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/predict_wage' \
     -H 'Content-Type: application/json' \
     -d '{"years_of_experience": 5}'
```

### **Python Request**
```python
import requests

response = requests.post("http://127.0.0.1:8000/predict_wage", json={"years_of_experience": 5})
print(response.json())
```

---

## **5️⃣ Running Tests**
Execute the test suite using `pytest`:
```bash
PYTHONPATH=. pytest
```

---

## **6️⃣ Run Pre-commit Hooks**
Ensure code follows style and linting rules before committing:
```bash
pre-commit run --all-files
```

---

## **7️⃣ Project Structure**
```
/app
  ├── main.py              # FastAPI application entry point
  ├── models.py            # Model definition (if applicable)
  ├── utils.py             # Utility functions
  ├── __init__.py          # Package initialization
  ├── tests/               # Test cases
├── requirements.txt       # Dependencies
├── requirements.in        # pip-compile dependencies
├── Dockerfile             # Containerization setup
├── docker-compose.yml     # Docker Compose config
├── .pre-commit-config.yaml # Pre-commit hooks
├── config.yaml            # Configuration settings
├── .gitignore             # Git ignore file
└── README.md              # Documentation
```

---

## **8️⃣ Docker Setup (Optional)**
### **8.1 Build and Run**
```bash
docker build -t fastapi-wage-api .
docker run -p 8000:8000 fastapi-wage-api
```

### **8.2 Using Docker Compose**
```bash
docker-compose up --build
```

---

## **9️⃣ Environment Variables (If Needed)**
Use a `.env` file for sensitive configurations:
```plaintext
SECRET_KEY="your_secret_key"
DEBUG=True
```
Then, load it in Python using `pydantic`:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    debug: bool = False
```

---

## **🔟 Azure DevOps CI/CD Pipeline**
If using **Azure DevOps**, add a `azure-pipelines.yml` file with a basic pipeline:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.9'
      addToPath: true

  - script: |
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
    displayName: 'Install dependencies'

  - script: |
      PYTHONPATH=. pytest
    displayName: 'Run tests'

  - script: |
      pre-commit run --all-files
    displayName: 'Run Pre-commit Hooks'
```

---

### ✅ **Improvements Made**
✔ **Added missing details** (Docker, API docs, Azure DevOps CI/CD)  
✔ **Formatted project structure for clarity**  
✔ **Improved API testing instructions**  
✔ **Pre-commit hook usage**  
✔ **Best practices for dependency management (`pip-compile`)**  

Your README is now **clean, structured, and deployment-ready**! 🚀  
