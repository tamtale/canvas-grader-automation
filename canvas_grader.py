import requests
import sys
import argparse

# base URL of the Canvas API
CANVAS_BASE_ENDPOINT = "https://canvas.rice.edu/api/v1/courses/"


def enter_grades(netids, course_id, assignment_id, auth_token, grade):
    """
    Given a list of netIDs, find the given assignment for the given course
    and assign the given grade to all the students with that netID in Canvas.
    
    (sample Canvas URL: https://canvas.rice.edu/courses/20376/assignments/98559)

    Arguments:
        netids {list} -- 
            list of netIDs of students to assign the grade to
        course_id {string} -- 
            ID of the course on Canvas (generally a 4-5) digit integer on 
            Canvas, i.e. '20376' in the example above
        assignment_id {string} -- 
            ID of the assignment on Canvas (generally a 4-5) digit integer on 
            Canvas, i.e. '98559' in the example above
        auth_token {string} -- 
            OAuth token generated from your Canvas account
        grade {string} -- 
            string representation of the numeric grade to assign the students
    """

    # get all student data for all students enrolled in the given course
    students = get_students_by_course_id(course_id, auth_token)

    if not students:
        # if there aren't any students in the course, there's some error, 
        # so terminate the program
        print("[ERROR] No students enrolled in given course, terminating...")
        return

    # get the Canvas-specific user IDs for all students that are to be graded
    user_ids = get_user_ids_from_netids(netids, students)

    # format each Canvas-specific user ID into the format expected by the 
    # Canvas API: "grade_data[<user_id>][posted_grade]"
    param_keys = \
        ["grade_data[" + str(uid) + "][posted_grade]" for uid in user_ids]

    # create the payload for the POST request: keys containing Canvas user IDs
    # and the grade instructions, mapped to the grade value to be assigned
    params = {k: str(grade) for k in param_keys}

    # create the necessary headers, including the authentication token
    headers = {
        "Authorization": "Bearer " + auth_token
    }

    # create the endpoint to send the request to 
    endpoint = CANVAS_BASE_ENDPOINT + str(course_id) 
    endpoint += "/assignments/" + str(assignment_id)
    endpoint += "/submissions/update_grades"

    # send the POST request to the endpoint with the given headers and payload
    response = post_to_endpoint(endpoint, headers, params)
    
    print("Response from endpoint: ", response)


def get_user_ids_from_netids(netids, student_data):
    """
    Given a list of netIDs and a list of data for all students in a class,
    finds all students whose netIDs are in the given list. Extracts their 
    Canvas user IDs from the detailed info and returns a list of those.
    
    Arguments:
        netids {list} -- 
            a list of netIDs for students you want to grade
        student_data {list} -- 
            list of dictionaries, where each dictionary contains detailed 
            student data from Canvas
    
    Returns:
        list -- 
            a list of the Canvas user IDs corresponding to the inputted netIDs
    """

    # filter out students whose netID is not in the inputted list
    students_matching_netids = \
        [s for s in student_data if s["login_id"] in netids]
    
    # extract the Canvas user IDs from the detailed info of the filtered 
    # students
    user_ids = [s["id"] for s in students_matching_netids]

    return user_ids


def get_students_by_course_id(course_id, auth_token):
    """
    Given a Canvas course ID, gets all accessible information about the users 
    in that course.
    
    Arguments:
        course_id {string} -- 
            course ID of the course you're trying to access
        auth_token{string} -- 
            authentication token generated by Canvas to pass along with POST 
            request
    """ 

    # the Canvas endpoint to hit
    endpoint = CANVAS_BASE_ENDPOINT + str(course_id) + "/users"

    # necessary headers for the request, including the OAuth authentication 
    # token generated from Canvas
    headers = {
        "Authorization": "Bearer " + auth_token
    }

    # boolean to keep track of whether or not there are more users left to find
    pages_left = True

    # keeps track of the current page number of users
    page_num = 1

    students = []

    while (pages_left):
        # iterate while there are still students left to find

        # create request payload with desired parameters
        payload = {
            "page": page_num,  # get all results from the given page
            "enrollment_type": "student"  # only find students
        }

        # send the GET request to the endpoint
        response = get_from_endpoint(endpoint, headers, params=payload)

        if (type(response) != list):
            # TODO: Add better error-handling here
            return 
        
        # add all student details to the existing list
        students.extend(response)

        # if the response was empty, there are no more students left, so this 
        # evaluates to False. If it was not empty, this evaluates to True.
        # Once there are no more students left, this ends the iteration of the
        # while loop.
        pages_left = bool(response)

        # increment the page counter
        page_num += 1

    return students


def run():
    """
    Runs the program, taking in optional command-line args.
    """

    # TODO: make command-line argparsing more robust - right now, it's 
    # hardcoded to correspond to the specific grading use case

    # instantiate the argument parser
    ap = argparse.ArgumentParser()

    # add a required OAuth token flag
    ap.add_argument("-at", "--auth-token", required=True, \
        help="OAuth token generated from your Canvas account")
    
    # add a required course ID flag
    ap.add_argument("-cid", "--course-id", required=True, \
        help="The course ID of the Canvas course you're trying to access")

    # add a required assignment ID flag
    ap.add_argument("-aid", "--assignment-id", required=True, help=\
        "The assignment ID of the Canvas assignment you're trying to access")

    # add a required netIDs flag - netIDs must be specified as a single string,
    # no spaces, individual netIDs separated by commas only
    ap.add_argument("-n", "--net-ids", required=True, \
        help="The netIDs of the students you're trying to bulk-grade, as a " \
            + "comma-separated string of values")
    
    # add a required flag for the grade value to assign to the students
    ap.add_argument("-g", "--grade", required=True, \
        help="The grade you wish to assign to the specified students")

    # parse the entered arguments from the command-line
    args = vars(ap.parse_args())

    auth_token = args["auth_token"]
    course_id = str(args["course_id"])
    assignment_id = str(args["assignment_id"])
    netids = args["net_ids"].split(",")
    grade = str(args["grade"])

    # enter the given grade for the given course assignment for the given 
    # students
    enter_grades(netids, course_id, assignment_id, auth_token, grade)


def get_from_endpoint(endpoint, headers=None, params=None):
    """
    Given an endpoint, optional headers, and optional request parameters, sends 
    a correctly formatted GET request to that endpoint with the given headers 
    and request params. If the request is successful, returns the JSON 
    response, otherwise, prints error messages to the console.
    
    Arguments:
        endpoint {string} -- 
            the endpoint URL to send the GET request to 
    
    Keyword Arguments:
        headers {dictionary} -- 
            optional header key-value pairs (default: {None})
        params {[type]} -- 
            optional request parameters as key-value pairs (default: {None})
    
    Returns:
        dictionary/list -- 
            the JSON object/array contained in the response, converted to a 
            Python object
    """


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
        endpoint {string} -- 
            The endpoint to send the request to
        headers {dictionary} -- 
            A dictionary containing header key-values
        payload {dictionary} -- 
            A dictionary containing body parameter key-values
    
    Returns:
         dictionary/list -- 
            the JSON object/array contained in the response, converted to a 
            Python object
    """


    response = requests.post(endpoint, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("[POST] Success POSTing to endpoint: ", endpoint)
        return response.json()
    
    print("[POST] Error POSTing to endpoint: ", endpoint)
    print("[POST] Status Code: ", response.status_code)
    print("[POST] Error Message: ", response.json())

# run the program driver
run()