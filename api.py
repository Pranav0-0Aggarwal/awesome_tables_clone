# Import necessary modules and packages
from flask import Flask,request,jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_caching import Cache

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing to allow requests from other domains
CORS(app)

# Create a cache instance
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Use the credentials to create a client to interact with the Google Drive API
# Specify the scope of access for the credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Load the credentials from the JSON file and authorize the client with the specified scope
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Add link to your spreadsheet here
# Open the spreadsheet by its URL and get the first sheet
spreadsheet_url = "link to your spreadsheet after clicking on the share button"
spreadsheet = client.open_by_url(spreadsheet_url)

# Define a helper function to check if a given pattern is present in a text
def is_present(text, pattern):
    str = text
    if str.find(pattern) != -1:
        return True
    else:
        return False

# Define a function to get the data from the Google Sheet
# Cache the data for an hour to reduce the number of API requests
@cache.cached(timeout=3600)
def get_data_from_sheet():
    sheet = spreadsheet.sheet1
    data = sheet.get_all_values()
    return data

# Define a route to return a simple message
@app.route('/',methods=['GET'])
def get_data():
    return 'Hello World !'

# Define a route to return the list of distinct subjects from the Google Sheet
@app.route('/subjects', methods=['GET'])
def get_subjects():
    data = get_data_from_sheet()
    subjects = set()
    counter = 0
    for row in data:
        # Skip the first row (header)
        if counter == 0:
            counter = 1
            continue
        # Convert the subject to uppercase and remove leading/trailing whitespaces
        subjects.add(row[3].upper().strip())
    # Convert the set to a list and return it as a JSON response
    return jsonify(list(subjects))

# Define a route to return the filtered and paginated list of books from the Google Sheet
@app.route('/data',methods=['POST'])
def show_data():
    global dict_search
    data = get_data_from_sheet()
    incoming_data = request.get_json()
    PageNo = incoming_data.get('page')
    BookAccNo = incoming_data.get('accNo')
    BookName = incoming_data.get('title')
    BookAuthor = incoming_data.get('author')
    BookSubject = incoming_data.get('subjectType')
    BooksList = []
    limst_1 = []
    limst_2 = []
    limst_3 = []
    iter = 1
    # If no filters are applied, return all the books
    if not BookAccNo and not BookName and not BookAuthor:
        lunt=0
        for iter in data:
            if lunt==0:
                lunt=1
                continue
            acc=iter[0]
            bookname=iter[1]
            bookauthor=iter[2]
            booksubject=iter[3]
            json_output = {'accNo':acc,'title':bookname,'author':bookauthor,'subjectType':booksubject}
            if BookSubject:
                if booksubject.lower()==BookSubject.lower():
                    BooksList.append(json_output)
            else:
                BooksList.append(json_output)
    else:
        while iter < len(data):
            counter=0
            acc=data[iter][0]
            bookname=data[iter][1]
            bookauthor=data[iter][2]
            booksubject=data[iter][3]
            json_output = {'accNo':acc,'title':bookname,'author':bookauthor,'subjectType':booksubject}
            if str(BookAccNo).lower()==str(acc).lower() and BookAccNo and acc!=None:
                counter=counter+1
            if is_present(bookname.lower(),BookName.lower()) and BookName and bookname!=None:
                counter=counter+1
            if is_present(bookauthor.lower(),BookAuthor.lower()) and BookAuthor and bookauthor!=None:
                counter=counter+1
            iter+=1
            if counter>=3:
                if BookSubject:
                    if booksubject.lower()==BookSubject.lower():
                        limst_3.append(json_output)
                else:
                    limst_3.append(json_output)
            elif counter==2:
                if BookSubject:
                    if booksubject.lower()==BookSubject.lower():
                        limst_2.append(json_output)
                else:
                    limst_2.append(json_output)
            elif counter==1:
                if BookSubject:
                    if booksubject.lower()==BookSubject.lower():
                        limst_1.append(json_output)
                else:
                    limst_1.append(json_output)
        BooksList=limst_3+limst_2+limst_1

    PageNo=int(PageNo)
    iter = (PageNo-1)*20
    limit = PageNo*20
    TotalPages=len(BooksList)
    BooksFinalList=[]
    while iter<limit and iter<TotalPages:
        BooksFinalList.append(BooksList[iter])
        iter+=1
    return [{'MaxPage':int(TotalPages/20)+(TotalPages%20!=0)},{'BookList':BooksFinalList}]

if __name__ == '__main__':
    app.run(debug=True,port=5000)
