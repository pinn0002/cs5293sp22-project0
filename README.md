****Name: Divya Sai Pinnamaneni****

****Run procedure:****

Install all the below-mentioned modules using pip install modulename

Install pipenv using pip install pipenv

Run the python main file using pipenv run python project0/main.py --incidents <url>

Run testfiles using pipenv run python -m pytest

****Observations****
>Every first page of pdf file contains title 'NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)' which needs to be removed

>At the end of each pdf file there is a date and time which needs to be skipped

>Multiline values are separated by ' \n'

>Null values are available only in 3, 4 columns together

****Expected bugs****

1. If rows in incident report pdf is missing one or more than two values, then the null values cannot be replaced with NA.
2. If title of the incident report pdf changed, this code doesn't replace 'NORMAN POLICE DEPARTMENT' and 'Daily Incident Summary(Public)' thus skips the last row to the count of nature as length of the row will become greater than 5.

**Libraries used in this project:**

argparse
urllib.request
tempfile
PyPDF2
re
sqlite3
pandas

****Project Objective:****

Aim of this project is to build python code to extract an incident report pdf from the Norman Police department's official website and extract all nature of incidents along with its count of occurrences throughout the report. To perform this operation I need to follow below steps and I have used a function in this code for each of the below step.
1. Download the incident report pdf
2. Extract the fields: Date/ Time, Incident Number, Location, Nature, Incident ORI data from pdf
3. Create a database to store the data. And the table should contain the fields described in step 2
4. Insert the data extracted from step 2 to the database created in step3
5. Print each nature o incident and number of times it occurs.

For this purpose, two python files are used. One is "main.py" to call the functions defined in "project0.py"
****main.py****

This file is used to extract the data and display the output. By calling this function, it will download and insert into database and prints the incidents summary.
This file uses argparse to pass arguments --incidents and <url> of the incident pdf. And this code is executed with the command - pipenv run python project0/main.py --incidents <url>

using import project0, all functions defined in project0 are extracted to main file.
project0.fetchincidents(url): to download incident report pdf
project0.extractincidents(incidents_data): extract incidents data in the form of list
project0.createddb(): To create a new database
project0.populatedb(db,incidents): To insert extracted incidents data to the created database
project0.status(db): To print the summary of incidents 

****project0.py****

**fetchincidents(url):**

It takes the url as input and uses urllib module to read the data from the url. This function returns the data read from url and this data is assigned to the incident_data in the main.py ile.

**extractincidents(incident_data):**

This function takes the input the extracted from fetchincidents(url) and using tempfile library writes pd data to a temporary file.
And to read this pdf data, use pdfReader from PyPDF2 module. Use getNumpages(), to find out the total page count of pdf. 
Extract the text from page1 and remove title in the first page i.e NORMAN POLICE DEPARTMENT\n and Daily Incident Summary (Public)\n by using replace function to make these values to empty. 
As there maybe a chance for multi-lines, use replace function to handle multiline text i.e. replace ' \n' with '' and use the same function in remaining pages too also append all pages together. use rstrip to remove the extra space received at the end of file.
Use re.split from the re module to split the page data for every date and time occurrence. In the regular expression \d{1,2} is used to represent occurrence of one or two digits and \d{4} is for representing 4 occurrence of digits, \s is for whitespace character in the below function.

page = re.split(r'\s+(?=\d{1,2}/\d{1,2}/\d{4}  \d{1,2}:\d{1,2})', page)

Create an empty list named pagelist. Skip the column header and split the remaining lines for every newline using re.split.
After each split, if length of list is 3 then extend the list to 5 with value 'NA' then exchange list item 5 and list item 3 and then append it to pagelist. Else if length of list is 5 then directly append it to the pagelist.
Then, return final pagelist to the function. And this pagelist is assigned to the incidents variable in main.py.

**createdb():**

Create a connection which represents the database and store the data in 'normanpd.db' using sqlite3 module. Create a cursor object and call execute method to drop the table i already exists and create a table incidents if not exists with the given schema.
CREATE TABLE incidents(incidents_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT)
Save the change and close the database.

**populatedb(db,incidents):**

This function takes the database created in createdb() and the incidents data extracted from extractincidents(incident_data) as input parameters. Then, connects to the database 'normanpd.db' and using cursor() object all the data is now inserted into the database using executemany statement. Once data is inserted save the changes in database and close the database.

**status(db):**

This function takes the input argument as database and prints the nature and count(nature) from incidents table. 
For this, first connect to the database and then use pandas module to read the below sql query 
SELECT nature, COUNT(nature) from incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature ASC
As the requirement is to display the count in descending order and nature should be in alphabetical order, I have used ORDER BY COUNT(nature) DESC and nature ASC.
Now, join the nature and count(nature) using pipe character(|) . As, dataframe contains index column change the dataframe to string and set the index to False for removing index column.

****test_project0.py****

To test all functions defined in project0.py, use test_project0.py to test each functionality in the functions. 
I have taken a testurl variable which takes incident report pdf URL and dbname takes 'normanpd.db' value.
**test_fetchincidents():**

In this function, I'm testing if the result of project0.fetchincidents(testurl) has some value in it or not by using assert is not None statement. As the function returns data, this testcase works for assert is not None.

**test_extractincidents():**

In this function, I'm testing if the return object type of project0.extractincidents(incident_data) is list or not. For this, use isinstance function to check the return object is list or not.

**test_createdb():**

In this function, I'm testing if the database name created in the project0.createdb() matches with the dbname initialized at the start of this test function.

**test_populateddb():**

Through this function, I'm calling a sql query to select values from incidents and testing whether data is available or not. I have used the select statement because in the original function we are inserting values so select statement should contain data.

**test_status():**

By this function, I'm testing if by executing SELECT statement returns some data or not.

****test_extractandstatus.py****

In this test file, I'm testing two functions extractincidents() and status()

**test_extractincidents():**

By this function, I'm testing if the length of the list is 5 or not by using assert statement. By this, I want to test if length of list as 5 because rom our main function we are only appending list if length is 5.

**test_status():**

Through this function, I want to test if the result is [] by executing DELETE FROM incidents. As DELETE removes all data, so it should return [] 









