import requests

# URL of your FastAPI endpoint
url = "http://localhost:8000/tables"

# Send a GET request to the FastAPI endpoint
try:
    response = requests.get(url)
    
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        print("FastAPI is running successfully!")
        print("Response data:", response.json())  # Print the JSON response from the endpoint
    else:
        print(f"Error: Received status code {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
