import requests

# The URL of our running prediction service
API_URL = "http://127.0.0.1:8000/predict"


def test_prediction_endpoint():
    """
    Integration test for the /predict endpoint.
    This test requires the Docker container for the prediction service
    and the local MLflow server to be running.
    """
    # Sample customer data for the request payload
    sample_customer = {"tenure": 10, "monthlycharges": 50.0, "totalcharges": 500.0}

    # Send a POST request to the API
    response = requests.post(API_URL, json=sample_customer)

    # Assertions: Check if the API responds correctly
    assert response.status_code == 200

    response_json = response.json()
    assert "churn_prediction" in response_json
    assert response_json["churn_prediction"] in [0, 1]
