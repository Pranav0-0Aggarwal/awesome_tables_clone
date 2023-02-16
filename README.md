awesome\_tables\_clone
======================

Book Catalog API

This is a Flask-based API to retrieve data from a Google Sheets book catalog. It supports filtering by book title, author, subject, and accession number, and returns a paginated response.

API Endpoints
-------------

*   GET /: Returns a simple "Hello World!" message.
*   GET /subjects: Returns a list of unique subject types in the catalog.
*   POST /data: Retrieves book data based on specified filters.

Required Dependencies
---------------------

This project requires the following Python dependencies:

*   Flask
*   Flask-Cors
*   Flask-Caching
*   gspread
*   oauth2client

You can install these dependencies by running:

    pip install -r requirements.txt

Configuration
-------------

Before running the API, you need to create a credentials.json file for authentication with Google Sheets. Here are the steps to generate the required credentials:

1.  Go to the Google Cloud Console.
2.  Select your project (or create a new one).
3.  Click on the hamburger menu in the top-left corner and go to APIs & Services > Credentials.
4.  Click the "+ CREATE CREDENTIALS" button and select "Service account key".
5.  Fill out the required fields and select "JSON" as the key type.
6.  Click "Create" to generate the credentials file.

Once you have your credentials.json file, replace the placeholder file in the project root directory.

You also need to specify the link to your Google Sheets document in the spreadsheet\_url variable in the app.py file.

Deployment on Render.com
------------------------

You can deploy this API on Render.com by following these steps:

1.  Fork this repository to your own GitHub account.
2.  Create a new web service on Render.com and connect it to your forked repository.
3.  In the "Environment" section, add a new environment variable with the key FLASK\_APP and the value app.py.
4.  In the "Environment" section, add a new environment variable with the key FLASK\_ENV and the value production.
5.  In the "Advanced" section, add a new file to the "Environment Variables" with the name CREDENTIALS\_JSON and the contents of your credentials.json file.
6.  Click "Create Web Service" to deploy the API.

Notes:

*   This API is configured to use a simple caching mechanism provided by Flask-Caching. The cache timeout is set to one hour by default, but you can adjust it by changing the timeout parameter in the cache.cached() decorator.
