import requests
import json
# Firebase project settings

with open('serviceAccountKey.json', 'r') as file:
    auth_key = json.load(file)

def manage_data(entity, operation, id, data=None, updates=None, database_url='https://masterdatabase-4a5d1-default-rtdb.firebaseio.com/'):
    endpoint = f"{database_url}{entity}/{id}.json?auth={auth_key}"
    if operation == 'write':
        # Writing or Overwriting data
        response = requests.put(endpoint, json.dumps(data))
    elif operation == 'read':
        response = requests.get(endpoint)
    elif operation == 'update':
        # Updating data
        response = requests.patch(endpoint, json.dumps(updates))
    else:
        print("Invalid operation")
        return

    # Print the result or error
    if response.status_code not in {200, 204}:
        print(f"Failed to {operation} data: {response.status_code}, {response.text}")
    else:
        print(f"Success: {operation} operation.")
        return response.content
