# canvas-grader-automation
A library of functions that can be run from the command-line, allowing graders on Canvas to automate several tedious tasks. Currently built for allowing large-scale automation of data-entry style grading where the same grade (eg. attendance credit) needs to be given to multiple students at once.

## Prerequisites
```
pip install -r requirements.txt
```

## Current Functionality
1. Currently, the script is capable of taking a Canvas course ID, an assignment ID, a grade, and a list of netIDs, and using the Canvas API to assign all students corresponding to those netIDs the chosen grade.
2. To do this, the app requires an authentication token, which you can generate through Canvas by:
    - going to Canvas -> Account -> Settings
    - Scrolling down and clicking on 'New Access Token' - add whatever purpose you'd like and copy the token into some local file where you can access it later.
3. After you have the authentication token, all you need to do is create a JSON file that contains the relevant information. The format of the JSON object should exactly match the sample JSON object in sample-config.json. 
    - I'd recommend naming your personal config file 'config.json' since that name is ignored by the .gitignore file, meaning no chance of accidentally committing your auth token to GitHub.
4. Fill out the config file with the relevant information and save it. 
5. Run the program from the command line (`python canvas_grader.py`) and specify an optional config filename if you'd like (`-f filename.json`)
6. Hopefully this should update the grades for all students you listed!

## Future Extensions
This script is currently limited to a single specific use case, but it could be interesting to explore other, more generalizable options.

## Bugs/Issues/Feature Requests
Feel free to open issues for bugs/feature requests on GitHub and tag them with the appropriate labels!
