# Tournament Results

This project is designed to capture the results of tournament outcomes, it does not utilize any external libraries. The database was developed using PostgreSQL and all programs use Python. Tournament Results is comprised of three files:

* `tournament.py`: a program that houses all relevant functions needed to properly execute a Swiss Pairings style tournament.
* `tournament.sql`: a database that houses all required information for `tournament.py` to execute properly, most notably tables to keep track of player information as well as match outcomes.
* `tournament_test.py`: a file as a mock tournament to adequately test all functions of `tournament.py` as well as the database tables of `tournament.sql`.

## Installation

After ensuring Python is installed on your local or virtual machine, in order to run this program:

1. Navigate to the directory in which you want to install Tournament Results.
2. Clone this repository to that directory.
3. Run `python tournament_test.py` to ensure all functions and database tables are properly working.
4. Create a new Python File and ensure to include `from tournament import *` at the top of the file.
5. Use `tournament_test.py` as a template to understand how to properly load your tournament data in to your new file.
6. Run `python your_file_name_here.py`.

Cloning from this repository will ensure that you always have the most up to date version of this software.

## Authors

Jasen Carroll  
jasen.c8@gmail.com  
July 31st, 2015

## Issues & Feature Requests

Please use GitHub to notify me of any issues or feature requests. 

* Navigate to the repository on [GitHub](https://github.com/jasenc/tournament_results).
* Click the `Issues` link on the menu towards the right.
* Then click `New issue`.

Pull Requests are encouraged! Please do no hesitate.


