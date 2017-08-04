# phddb

MEASURING THE IMPACT OF PHD THESES

A set of scripts that is scraping, following and analyzing the doctoral theses that are written in Finland.
Target is the webservice Melinda of Finnish National Library. The goal is to provide useful statistics, e.g. about the gender of the authors, language use, distribution of theses between universities, and many more. An impact factor will be calculated that grades article-based theses based on a dynamic ratio between citation counts of the individual publication (retrospectively) and the journal impact factor (prospectively), depending on how many years ago the articles of the thesis have been published. 

DISCLAIMER
The code is not elegant (= terrible). Our aim was to get the job done, because we were interested in the results. Once a script did its job without errors, we called it a day and moved to the next part of the project. Most of the scripts need to do run over the whole time period (e.g. 1980 - 2017) only once, and after that only increamental updates are needed and thus performance is not an issue. Improvements are nevertheless welcome!

MAIN THINGS UNDER DEVELOPMENT

1. PDF extractor: For most theses, the full text is freely available as PDF file. Article-based theses enumerate the articles that have been used for the thesis on a dedicated page. We need to write a script, that can find this page from the PDF and extract the bibliographic data and put it into a database.
2. Citation retriever: Once we have the list of all publications (provided by the PDF extractor), we need to go to online databases and figure out how many publications each publication has received for any given year and put this data into a database.

LICENSE
phddb is distributed under the GNU General Public License v3.0.

REQUIREMENTS
phddb has only been tested on Ubuntu 16.04. It requires the following packages to be installed:

- python3 (is by default already included in Ubuntu 16.04) 
- mariadb-server (or mysql-server; if you install the mariadb server, be aware that it doesn't ask to set a root password during the install; however, (system) root can execute mysql-root commands (see below).
- python3-mysqldb
-
phddb uses the following modules: requests, time, re, random, sys, os. All of them should be installed by default on Ubuntu 16.04.

INSTALLATION
The only thing you need to do before starting the script is to prepare the database by executing either of the following two commands:
$ mysql -u root -p < phddb.sql (mysql-server)
$ sudo mysql -u root < phddb.sql (mariadb-server)

SCRIPT EXECUTION (RETRIEVAL OF THESES)
$ python3 fin_phd_theses_scarper.py

ANALYSIS (ADDING GENDER INFORMATION)
To assign a gender to each entry in the theses table, you need to load first the data in the firstnames.sql file into the database:
$ mysql -u phddb_user -p < phddb_firstnames.sql
Then you need to execute the determine_gender.py script:
$ python3 determine_gender.py

SUPPORT
This project has been generously supported by the Finnish Cultural Foundation.

