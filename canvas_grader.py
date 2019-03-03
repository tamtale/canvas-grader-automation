import requests
import sys

CANVAS_BASE_ENDPOINT = "https://canvas.rice.edu/api/v1/courses/"

def run():
    """
    Runs the program, taking in optional command-line args.
    """

    # TODO: make command-line argparsing more robust - right now, it's 
    # hardcoded to correspond to the specific grading use case

    auth_token = sys.argv[1]


def get_from_endpoint(endpoint, headers=None):

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        print("[GET] Successfully retrieved response from endpoint: ", endpoint)
        return response.json()

    print("[GET] Error GETting from endpoint: ", endpoint)
    print("[GET] Status Code: ", response.status_code)
    print("[GET] Error Message: ", response.json())


def post_to_endpoint(endpoint, headers, payload):
    """

    Given an endpoint, headers, and a request body, sends a correctly formatted
    POST request to that endpoint with the given headers and body. If the 
    request is successful, returns the JSON response, otherwise, prints error
    messages to the console.
    
    Arguments:
        endpoint {[string]} -- The endpoint to send the request to
        headers {[dictionary]} -- A dictionary containing header key-values
        payload {[dictionary]} -- A dictionary containing body parameter key-
            values
    
    Returns:
        [dictionary] -- The JSON format contained in the response
    """


    response = requests.post(endpoint, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("[POST] Success POSTing to endpoint: ", endpoint)
        return response.json()
    
    print("[POST] Error POSTing to endpoint: ", endpoint)
    print("[POST] Status Code: ", response.status_code)
    print("[POST] Error Message: ", response.json())

run()