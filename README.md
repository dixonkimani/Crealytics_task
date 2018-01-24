# Crealytics_task
Crealyitcs DevOps task

The file gcp_api.py uses flask to create an API endpoint with multiple methods.

Installation:
1) Install pip3
  Ubuntu: sudo apt-get install python-pip3

2) Install the Google cloud python library
  Ubuntu: pip3 install google-api-python-client

3) Install flask
  Ubuntu: pip3 install flask

4) In your Google Cloud Platform account create an API key. Go to
  API Keys Menu > Create Credentials > Service Account Key > JSON > Save the key file

5) Create the environment variable for Google Cloud Platform authentication
  Ubuntu: Add the following to either /etc/profile or ~/.profile
  export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE

6) Ensure that startup.sh file is in the same directory as the gcp_api.py


Running:
1) To run the API script
  python3 /path/to/gcp_api.py

Usage:
To access the API from the local system:

curl -i http://localhost:5000/METHOD

Methods:
/healthcheck - [GET] Returns only a 200 response
/v1/instances/create/<project>/<zone>/<name>/<username>/<password> - [POST] Creates a compute
    instance based on the provided params and Returns NAT IP address
