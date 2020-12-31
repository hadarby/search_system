# Text Search Project

### Implementing a Search Engine with Ranking Results in Python and MongoDB
##### Final project for 'Search System and Recommendations' - Tel Aviv university 

##### Description: 
This search project demonstrates text search by positional index.
<br/>
The results are first the files where all the search words were found and then the files with some of the words.
<br/>
The internal sort is by the frequency of the word/s.
<br/>
You may want to modify some of the configurations and files as needed. 
   
###
##### Keywords: 
python, search, text files, project, mongodb, pymongo, setup, development, university, education.
###

##### By Hadar Ben-Yaakov
[LinkedIn](https://www.linkedin.com/in/hadar-ben-yaakov/)
##
 
### Setup and run instructions:

#### Prerequisites:
`pip install -r requiremenets.txt`
<br/>

#### Configurations:
1. Create user on MongoDB cloud
2. Paste your connection string as value of: mongo_connection_string on the run files.
3. You can replace the lyrics folder with a folder with text file of your choosing.<br/>Just remember to use the correct folder name when you create TextFiles() instance.
4. Choose the level of logs you want to receive in the run files.
<br/>
 
#### Run:
 Run the project with your IDE's configuration, or from the terminal.
 
 ##
 
### Usage:
For advance actions with MongoDB use the wrapper - mongo_utils.py
