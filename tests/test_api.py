import requests
import json

# Define the URL of your Flask application's endpoint
api_url = (
    "https://piql-aec8f86e81c3.herokuapp.com/add_item"  # Replace with your actual URL
)

# Define the data you want to send in the request
item = {"name": "Example Item"}

# Convert the item data to JSON
headers = {"Content-Type": "application/json"}

# Make a POST request to add the item
response = requests.post(api_url, data=item, headers=headers)

# Check the response
if response.status_code == 200:
    print("Item added successfully.")
else:
    print("Error:", response.status_code)
    print(response.text)  # Print the response content for error details
