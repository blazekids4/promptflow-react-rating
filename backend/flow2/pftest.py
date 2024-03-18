import urllib.request
import json
import os
import ssl


data = {
    "input": "Is there an age one can be discriminated against?"
}

body = str.encode(json.dumps(data))

url = 'https://hrchat-pf.westus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'UY0AEqgnM6tzY6GG0JkHK0SMg5CM0dYK'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'hrchat-pf-1' }
print(headers)

print(body)
req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    print(response)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))