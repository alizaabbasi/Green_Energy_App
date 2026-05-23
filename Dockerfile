FROM python:3.10-slim

WORKDIR /app

# Install the minimal required Python libraries safely
RUN pip install fastapi uvicorn scikit-learn joblib pandas numpy

# Copy web application and model file into the cloud container image
COPY main.py .
COPY energy_router.joblib .

# Open port 8080 for web traffic routing
EXPOSE 8080

# Start up the web server automatically
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]