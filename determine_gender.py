#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This script uses a the firstnames table of the local database to add gender
# information to the theses tables according to the combined probability of
# thesis author's firstname(s). It can be executed once the fin_phd_theses_scraper.py
# has been executed. After the initial run, only incremental runs (for the current year)
# are needed to add gender information to the newly added theses.
# When the script is executed, it goes through the theses database and
# determines the gender of the author based on the local database. When the
# local database doesn't return an answer, it goes to genderize.io and tries
# to get an answer. genderize.io is limited to 1000 names/day, hence we limit
# the number of requests to 100 per run. This allows ten executions per day,
# which should be sufficient if you just check the newly added theses and
# don't update the complete database (the complete database contains at the
# moment stii more than 400 thesis authors of unknown gender).
#
# On Ubuntu 16.04 the following packages need to be isntalled: python3-mysqldb
#
import MySQLdb as phddb
import requests, time, re, json, random, sys
from phddb_lib import initialize_logfiles, finalize_logfiles, logfile, get_gender

# Connection credentials
sqlhost = 'localhost'
sqllogin = 'phddb_user'
sqlpassword = 'zdshDc6UZXnjUap6' #This needs to be changed if you want to be secure
sqldb = 'phddb'

# Create connection
sqlcon = phddb.connect(host=sqlhost, user=sqllogin, passwd=sqlpassword, db=sqldb, charset='utf8')

# Limit the run based on mysql request
#limit = '20'
#offset = '10'

# Limit the gender determination to theses by year: only
# theses from this year and later years will be included
year_limit = 1980

# This number increments when the theses database was updated
# based on a request result.
update_number = 0

# Initialize logfiles
logfilename = 'determine_gender'
logfilepath = initialize_logfiles(logfilename, 'LS')
logfile(logfilepath, 'LS', "<br>\n")

with sqlcon:
    # Preamble
    # This gets the database version
    cursor = sqlcon.cursor()
    cursor.execute("SELECT VERSION()")
    anzahl = cursor.fetchone()
    logfile(logfilepath, 'LSP', "Database version: %s " % anzahl)
    # This gets the number of theses entries, where the author's gender is unknown or controversial
    query = "SELECT COUNT(*) FROM theses WHERE (gender = 'unknown' OR gender = 'controv' OR gender IS NULL)"
    cursor.execute(query)
    anzahl_unknown_in_theses = cursor.fetchone()
    # Check how many entries are in the firstnames database
    query = "SELECT COUNT(*) FROM firstnames"
    cursor.execute(query)
    anzahl_total_in_firstnames = cursor.fetchone()
    # Check how many entries are in the firstnames database that are unknown
    query = "SELECT COUNT(*) FROM firstnames WHERE (gender_fi = 'unknown' OR gender_fi = 'controv' OR gender_fi IS NULL)"
    cursor.execute(query)
    anzahl_unknown_in_firstnames = cursor.fetchone()

    # Main query to get all unknown first names
    query = "SELECT melinda_id, author FROM theses WHERE (gender = 'unknown' OR gender = 'controv' OR gender IS NULL)"
    # Try to limit the mysql request based on the year limit
    try:
        year_limit
    except NameError:
        logfile(logfilepath, 'LSP', "Year limit not defined.")
    else:
        query += " AND date > '" + str(year_limit-1) + "-00-00'"
    # Try to append a mysql limit if it has been set
    try:
        limit
    except NameError:
        logfile(logfilepath, 'LSP', "Limit not defined.")
    else:
        query += " LIMIT "
    # Try to append a mysql offset if it has been set
    try:
      offset
    except NameError:
        logfile(logfilepath, 'LSP', "Offset not defined.")
    else:
        query += offset + ", "
    try:
        limit
    except NameError:
        logfile(logfilepath, 'LSP', "Limit not defined.")
    else:
        query += limit
    logfile(logfilepath, 'LSP', "Query = " + query)
    cursor.execute(query)
    logfile(logfilepath, 'LSP', "Number of records with unknown gender that we are now trying to determine: " + str(cursor.rowcount) + "\n")
    rows = cursor.fetchall()
    total_request_number = 0
    for row in rows:
        logfile(logfilepath, 'LS', "<br>\n")
        logfile(logfilepath, 'LSP', "\n" + str(total_request_number+1) + ". " + row[1])
        firstname = re.split(', ',row[1])
        logfile(logfilepath, 'LSP', "Split: " + str(firstname))
        # Remove last name
        firstname.pop(0)
        connector = "-"
        #firstnames_pruned = []
        firstnames = re.split('[ -]',connector.join(firstname))
        logfile(logfilepath, 'LSP', "Firstname(s): " + str(firstnames))
        # Remove all abbreviated firstnames NOT NEEDED, SINCE IT IS DONE IN THE FUNCTION get_gender
        #for name in firstnames:
        #    if ((len(name) == 2) and (name[-1:] == '.')):
        #        pass
        #    else:
        #        firstnames_pruned = firstnames_pruned + [name]
        #print("After removal:", firstnames_pruned)
        if len(firstnames) > 0:
            gender = get_gender(firstnames, logfilepath)
            total_request_number += 1
            logfile(logfilepath, 'LSP', "gender: " + gender)
            # Enter gender data into mysql
            query = "UPDATE theses SET gender = '" + gender + "' WHERE melinda_id = " + str(row[0]) + " AND (gender IS NULL OR gender = 'unknown' OR gender = 'controv')"
            try:
                cursor.execute(query)
                # Count when a gender entry in the theses database was updated
                if cursor.rowcount == 1:
                    update_number += 1
                sqlcon.commit()
            except phpdb.Error as e:
                if e[0]!= '':
                    raise
            print("\n")
        else:
            logfile(logfilepath, 'LSP', "Cannot determine gender based on abbreviated first name!")
    logfile(logfilepath, 'LS', "<br>\n")
    logfile(logfilepath, 'LSP', str(total_request_number) + ' requests made to identify gender based on first name.')
    logfile(logfilepath, 'LSP', str(update_number) + ' updates made to the theses database.')

    # This gets the number of theses entries, where the author's gender is unknown or controversial
    query = "SELECT COUNT(*) FROM theses WHERE (gender = 'unknown' OR gender = 'controv' OR gender IS NULL)"
    cursor.execute(query)
    anzahl_unknown_in_theses2 = cursor.fetchone()
    logfile(logfilepath, 'LSP', "Number of records with unknown gender in theses table before run: %s " % anzahl_unknown_in_theses)
    logfile(logfilepath, 'LSP', "Number of records with unknown gender in theses table after run: %s " % anzahl_unknown_in_theses2)
    # Check how many entries are in the firstnames database
    query = "SELECT COUNT(*) FROM firstnames"
    cursor.execute(query)
    anzahl_total_in_firstnames2 = cursor.fetchone()
    logfile(logfilepath, 'LSP', "Total number of first names in firstnames table before run: %s " % anzahl_total_in_firstnames)
    logfile(logfilepath, 'LSP', "Total number of first names in firstnames table after run: %s " % anzahl_total_in_firstnames2)
    # Check how many entries are in the firstnames database that are unknown
    query = "SELECT COUNT(*) FROM firstnames WHERE (gender_fi = 'unknown' OR gender_fi = 'controv' OR gender_fi IS NULL)"
    cursor.execute(query)
    anzahl_unknown_in_firstnames2 = cursor.fetchone()
    logfile(logfilepath, 'LSP', "Total number of unknown fist names in firstnames table before run: %s " % anzahl_unknown_in_firstnames)
    logfile(logfilepath, 'LSP', "Total number of unknown fist names in firstnames table after run: %s " % anzahl_unknown_in_firstnames2)
    cursor.close()
finalize_logfiles(logfilepath, 'LS')
