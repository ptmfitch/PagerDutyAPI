This package contains the solutions for the PagerDuty Solutions Consultant Technical Exercises using the python to make calls to the various APIs.

To execute any of the scripts, I would recommend setting up a virtual environment (I used pip) and installing the additional libraries contained in the requiements.txt file. I used python 3.6.5 to write the scripts.

You will also need to create a python file in this directory called "api_auth.py" containing your api_token and routing_key. The scripts won't work without these.

The scripts make heavy usage of the existing PagerDuty Python REST API Sessions library, which was a convenient way to get started quickly without worrying about writing boilerplate request and authentication code.
