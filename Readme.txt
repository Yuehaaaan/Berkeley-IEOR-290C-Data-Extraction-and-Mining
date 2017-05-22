Group Kiva Team

Team members:
Yichen Dong xinwangdemoli@126.com
Yuntian Bi  biyuntian@berkeley.edu
Yuehan Xu   xyh110191@berkeley.edu
Qingyu Wei  weiqing@berkeley.edu

File description and Readme

Project_Code.py
This file is used to scrappe all relevant information from the kiva team website and stores them in the appropriate csv files.
The page_num in setTeamLoans(KivaTeam) function is set to 10 due to time constraints but can be set to as high as 300
Team rankings will be set to 0 if the team does not have a ranking
New members this month and new loans made this month does not work properly

Impact Analysis.py
Requires all csv files created in Project_Code.py and "figures" directory
This file analyzes the data scrapped, producing max, mean, mode, std deviation, regression results, etc.
It also produces all relevant figures

MappingCountries.py
This file is used to create the map indicating the number of loans made to each country.
Requires country_location.json

MappingCountries_map2.py
This file is used to create the map indicating the number of members in each country.
Requires country_members.json

sql_script
This file is used to create the appropriate schema in MySql

MySql Description.txt
This file describes each table in the MySql database

Visualization
This folder contains python files generating charts. Runnning these python files requires all csv files.
