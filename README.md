# phddb

MEASURING THE IMPACT OF PHD THESES

A set of scripts that is scraping, following and analyzing the doctoral theses that are written in Finland.
Target is the web service Melinda of Finnish National Library. The goal is to provide useful statistics, e.g. about the gender of the authors, language use, distribution of theses between universities, and many more. An impact factor will be calculated that grades article-based theses based on a dynamic ratio between citation counts of the individual publication (retrospectively) and the journal impact factor (prospectively), depending on how many years ago the articles of the thesis have been published. Because there is no unified method to retrieve the full text versions of theses (which are mostly published as PDFs), the first implementation is limited to the University of Helsinki. This implementation uses the public data from https://ethesis.helsinki.fi, which is nearly complete since 2006 and which also contains standardized links to the public full text thesis files.

DISCLAIMER
The code is not elegant (= terrible). Our aim was to get the job done, because we were interested in the results. Once a script did its job without errors, we called it a day and moved to the next part of the project. Most of the scripts need to cover the whole time period (e.g. 1980 - 2017) only once, and after that only incremental updates are needed and thus performance is not an issue. Improvements are nevertheless welcome!

WHAT IS READY

1. Retrieval of all PhD theses published in Finland from Melinda: fin_phd_theses_scraper.py
The data is stored in the "theses" table of the phddb database.

2. Gender determination for all authors of PhD theses published in Finland: determine_gender.py
For about 1-2% of the thesis authors, the determination from a local database still fails and we will need to complete the data with personal communication. In the meantime, the script tries to complete missing gender data using the public and free API from https://genderize.io.

3. PDF retrieval from https://ethesis.helsinki.fi: get_UH_PhD_thesis_PDFs.py
This retrieves all thesis PDFs from https://ethesis.helsinki.fi for later processing by the PDF extractor.

MAIN THINGS UNDER DEVELOPMENT

1. While retrieving the PDFs from https://ethesis.helsinki.fi, the script should also populate missing fields
in the "theses" table (which were not available from Melinda, but which were available from https://ethesis.helsinki.fi). Maybe we have to add a few fields to the "theses" table, depending on what information we want to gather. We maintain at the moment a separate table in the phddb database for theses from https://ethesis.helsinki.fi (table "thesis", which is based on a database dump from ~2016), but the goal is to get rid of it and to migrate introduce meaningful fields into the "theses" table.

2. PDF extractor: For most theses, the full text is freely available as PDF file. Most article-based theses enumerate the articles that have been used for the thesis explicitly on a dedicated page. We need to write a script, that can find this page from the PDF and extract the bibliographic data and put it into a database.

3. Citation retriever: Once we have the list of all publications (provided by the PDF extractor), we need to go to online databases and figure out how many publications each publication has received for any given year and put this data into a database.

LICENSE
phddb is distributed under the GNU General Public License v3.0.

REQUIREMENTS
phddb has only been tested on Ubuntu 16.04. It requires the following packages to be installed:

- python3 (is by default already included in Ubuntu 16.04)
- mariadb-server (or mysql-server; if you install the mariadb server, be aware that it doesn't ask to set a root password during the install; however, (system) root can execute mysql-root commands (see below).
- python3-mysqldb

phddb uses the following modules: requests, time, re, random, sys, os, certifi. All of them are available on Ubuntu 16.04 and most of them even install by default (except certifi).

INSTALLATION
The only thing you need to do before starting the script is to prepare the database by executing either of the following two commands:
$ mysql -u root -p < phddb.sql (mysql-server)
$ sudo mysql -u root < phddb.sql (mariadb-server)

SCRIPT EXECUTION

1. Retrieval of all theses data:
$ python3 fin_phd_theses_scarper.py

2. Retrieval of all phd thesis PDFs from ethesis.helsinki.fi. This does not require the mysql database. It simply downloads all PDFs into the files/PDF subdirectory:

$ python3 get_UH_PhD_thesis_PDFs.py

3. Analysis, part 1 - Adding gender information. To assign a gender to each entry in the theses table, you need to load first the data in the firstnames.sql file into the database:

$ mysql -u phddb_user -p < firstnames.sql

Then you need to execute the determine_gender.py script:

$ python3 determine_gender.py

SUPPORT
This project has been generously supported by the Finnish Cultural Foundation.
