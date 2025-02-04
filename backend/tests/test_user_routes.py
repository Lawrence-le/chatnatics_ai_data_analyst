# backend\tests\test_user_routes.py

import pytest
from flask import Flask
from app.routes.user import user
from unittest.mock import patch


# Fixture to create and configure the Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(user)
    return app


# Fixture to create a test client for making requests to the app
@pytest.fixture
def client(app):
    return app.test_client()


# Test the user prompt route when OpenAI is disabled (No need to mock requests here)
def test_user_prompt_openai_disabled(client):
    # Define the test input where openai_status is False
    test_input = {
        "user_input": "Find the salary of nus graduates for year 2021",
        "openai_status": False,  # No AI assist for this test
    }

    # Send the POST request to the /prompt endpoint
    response = client.post("/prompt", json=test_input)

    # Assert the status code of the response
    assert response.status_code == 200

    # Get the response JSON
    response_json = response.get_json()

    # Print the response for debugging
    print("Response JSON (OpenAI Disabled):", response_json)

    # Assert the response content
    assert "user_prompt" in response_json
    assert response_json["user_prompt"] == test_input["user_input"]
    assert "process_response" in response_json
    assert "response" in response_json["process_response"]


# Test the user prompt route when OpenAI is enabled (Mock the requests.post method)
@patch("requests.post")  # Mock the requests.post method
def test_user_prompt_openai_enabled(mock_post, client):
    # Define the test input where openai_status is True
    test_input = {
        "user_input": "Find the salary of nus graduates for year 2021",
        "openai_status": True,  # AI assist enabled
    }

    # Mock the OpenAI API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "AI generated response"}

    # Send the POST request to the /prompt endpoint
    response = client.post("/prompt", json=test_input)

    # Assert the status code of the response
    assert response.status_code == 200

    # Get the response JSON
    response_json = response.get_json()

    # Print the response for debugging
    print("Response JSON (OpenAI Enabled):", response_json)

    # Assert the response content
    assert "user_prompt" in response_json
    assert response_json["user_prompt"] == test_input["user_input"]
    assert "process_response" in response_json
    assert "response" in response_json["process_response"]

    # Assert that OpenAI response was used
    assert response_json["process_response"]["response"] == "AI generated response"
