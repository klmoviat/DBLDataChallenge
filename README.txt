CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Installation
 * Running the program
  * Creating a fresh database
  * Working with the database
 * Last thoughts
 * Credits


INTRODUCTION
------------

This program can be used to analyze a set of tweets from a set of companies
after obtaining them from the twitter API. The program is initially made to
analyze the efficiency of the KLM twitter team, but can be used for other
teams in the future by simply creating a fresh database.

Most of the code is softcoded, meaning that it can be adapted quickly for 
future work. Some code (like a list of company ID's, and some of the
code for the graphs) is slightly hard coded with the names and id's
that were known beforehand, but these can be softcoded in the future.

The code was written in PyCharm in python, and uses sQlite as a database
manager. A full list of dependencies is given in the installation guide.


INSTALLATION
------------

In theory any python IDE can be used to run the program, but we recommend
sticking with PyCharm for this project as it has a nice sQlite database
manager interface and has been tested. Please note that PyCharm professional
is recommended, as it comes with a better UI to manage the sqlite databases. 

First off, make sure the python version 3.9 or up is installed on your machine.
Create a new project in PyCharm, and extract all files from this zip file
into the new project folder.

To make sure the programruns without errors, please install the following packages:
Package name: 		Version (or higher)
- DateTime		- v4.4
- matplotlib		- v3.5.2
- numpy			- v1.22.3
- pandas		- v1.4.2
- pip			- v22.0.4
- protobuf		- v3.20.x (This will fail on newer versions!)
- scipy			- v1.8.1
- seaborn		- v0.11.2
- sentencepiece		- v0.1.96
- SQL			- 2022.4.0
- tokenizers		- v0.12.1
- torch			- v1.11.0
- tqdm			- v4.64.0
- transformers		- v4.19.2


NOTE: in pycharm, packages can be installed by going to file (top-left)->
settings->project:xxx -> python interpreter and clicking the '+' button.


OPTIONAL: 
To skip loading in the data for the airlines using the program, simply use the
full, pre-analized database, available as "ALL_DATA.sqlite" from:
https://tuenl-my.sharepoint.com/:f:/g/personal/f_w_overbeeke_student_tue_nl/EpB5TC5jDjpImyD3pco6UeoBbUvfWgpszLe2qjdO7_bwrA?e=XE6cQC
(SeptData.sqlite can also be downloaded to only work with the month september)

OPTIONAL BUT RECOMMENDED:
It is highly recommended to add the sqlite databases to the database view in PyCharm.
This can be done by opening database from the toolbar on the right, and clicking the '+' icon.
From here, select datasource -> sqlite and then under general -> file click the
... icon to select the databases. This can be done for the DataChallenge.sqlite that
is included, as well as for the optional databases, and allows easy access to the
data stored in the databases.

That is all for installation.



Running the program
----------------
To run the program, simply right click on the main file and press run. It will
initialize the sentiment analysis variables first, which might take 15 seconds.
(NOTE: First time running this will take longer, as it has to download the all files
required for sentiment analysis!)
After this, a primitive user interface will guide the user through all operations.
Note that when using this interface, spelling (including capitalization) is 
very strict, and the program might crash when misspelling.


CREATING A FRESH DATABASE
-------------

The base file for a database (DataChallenge.sqlite) is included in the zip. By 
typing 'n' at the first input list, the program will run the script in 
'EFFICIENT_LOADING.py. Here, the folder that contains the JSON files
can be selected, and there is a follow up question that asks whether the full
database is to be run or just a specific part. This script will keep you updated
on the progression, and will return to the main.py script with a database 
that contains all the necessary tweet and user info.

NOTE: after the progressbar has finished, the script still takes some time
to create the actual database.


WORKING WITH THE DATABASE
-----------------

Now that there is a base database (or if you decided to work with an 
existing one), tables can be created with the conversation info of 
specific companies. To do this, select 'a' from the input menu, 
and type in the TWITTER USERNAME of the company. 

Now that one or several company tables are entered, sentiment analysis can
be run over the tables to get the starting, end and delta in sentiment
from the conversations. To do this, select 'e'. NOTE: this will take a while.
Only for KLM will the program use the dutch sentiment analysis method.

Finally, sentiment can be ran on all tweets that have no responses but do
mention either KLM, British Airways, Lufthansa or Ryanair. To do this, type
'm'. NOTE: THIS WILL TAKE VERY, VERY, VERY LONG! IT IS ADVICED TO JUST USE
ALL_DATA.sqlite WHICH HAS THIS PRELOADED

Once KLM, British_Airways, Lufthansa and Ryanair have been fully loaded in, 
the plots can be made by selecting 'p'. The plots will be saved in the
'Plots' folder that is included in the zip.



LAST THOUGHTS
---------------

Making some adjustments to the scripts would allow the program to be 
generalized for further research and other projects. As stated, the
main points are the plotting scripts having names hardcoded, and 
the company names being hardcoded. Adding some nice user interface 
would greatly assist in making the program more user friendly.

Additionally, sql server is a way better option performance wise, allowing
the database to be stored remotely and manipulated more quickly.


CREDITS
----------------
All credits go to group 22 from the course Data Challenge (JBG030) 2021/4
from the Technical University Eindhoven:
#################################################
#   Frank Overbeeke		1224268		#
#   Kyra Moviat			1349171		#
#   Mirthe de Goede		1700642		#
#   Roy van Heertum		1695126		#
#   Rhahim Gregoria		1629050		#
#################################################