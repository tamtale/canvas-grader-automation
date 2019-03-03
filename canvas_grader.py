import requests
import sys

CANVAS_BASE_ENDPOINT = "https://canvas.rice.edu/api/v1/courses/"


def enter_grades(netids, assignment_id, course_id, auth_token, grade):
    # TODO: Add documentation for this!

    pass


def get_user_ids_from_netids(netids, student_data):
    # TODO: Add documentation for this too LOL

    user_ids = []

    students_matching_netids = \ 
        [s for s in student_data where s["login_id"] in netids]
    
    user_ids = [s["id"] for s in students_matching_netids]

    return user_ids


def get_students_by_course_id(course_id, auth_token):
    """
    Given a Canvas course ID, gets all accessible information about the users 
    in that course.
    
    Arguments:
        course_id {[integer]} -- Course ID of the course you're trying to 
            access
        auth_token{[string]} -- Authentication token generated by Canvas to 
            pass along with POST request
    """

    # TODO: Add better documentation for this whole thing

    endpoint = CANVAS_BASE_ENDPOINT + str(course_id) + "/users"

    headers = {
        "Authorization": "Bearer " + auth_token
    }

    pages_left = True
    page_num = 1

    students = []

    while (pages_left):

        payload = {
            "page": page_num,
            "enrollment_type": "student"
        }

        response = get_from_endpoint(endpoint, headers, params=payload)

        if (type(response) != list):
            # TODO: Add better error-handling here
            return 
        
        students.extend(response)

        pages_left = bool(response)

        page_num += 1
    
    print(len(students))

    return students








def run():
    """
    Runs the program, taking in optional command-line args.
    """

    # TODO: make command-line argparsing more robust - right now, it's 
    # hardcoded to correspond to the specific grading use case

    auth_token = sys.argv[1]
    get_users_by_course_id(20376, auth_token)


def get_from_endpoint(endpoint, headers=None, params=None):

    response = requests.get(endpoint, headers=headers, params=params)

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