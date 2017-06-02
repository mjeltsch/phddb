#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Theses scraper for the Melinda database (Finnish National Library)
#
# What does it do?
#
# On Ubuntu 16.104 the following packages need to be installed: python-urllib3 and python3-mysqldb
#
# Command line arguments:
#
# An integer that determines how much to slow down the requests in order not to get blocked (default = 50),
# smaller is faster
#
import MySQLdb as phddb
import requests, time, re, random, sys, os

def substring_after(s, delim):
    if delim != '':
        return s.partition(delim)[2]
    else:
        return ''

def substring_before(s, delim):
    return s.partition(delim)[0]

# This takes a test (a webpage source) and searches until the occurence of substring_start. Then it searches
# onward for the next following occurence of substring_stop and returns the text in between both occurences.
def find_next_occurence(text,substring_start,substring_stop):
    if ((text != '') and (substring_start != '')):
        text_after_substring_start = substring_after(text, substring_start)
        return substring_before(text_after_substring_start,substring_stop)
    else:
        return ''

# This creates a logfile and prints to the screen. A variable number of
# strings (or lists of strings) can be passed to this function. If the
# first argument is equal to the string "also_to_short_logfile", the
# function also writes to a second (shorter) logfile.
def logfile(*write_tuple):
    #print("I was called with", len(arg), "arguments:", arg)
    # Write to short logfile if first list entry is the string "write_to_short_logfile"
    write_list = list(write_tuple)
    if write_list[0] == "write_to_short_logfile":
        tmp = open(short_logfilepath,"a")
        write_list.pop(0)
        for element in write_list:
            if type(element) is list:
                for item in element:
                    tmp.write("%s<br>\n" % item)
            else:
                item = element + "<br>\n"
                tmp.write(item)
        tmp.close()
    # Write to detailed logfile
    tmp = open(detailed_logfilepath,"a")
    for element in write_list:
        if type(element) is list:
            for item in element:
                tmp.write("%s<br>\n" % item)
        else:
            item = element + "<br>\n"
            tmp.write(item)
    tmp.close()
    print(write_list)

def sanitize_year(date):
    # Some weired year entries are like this: 1982-1992, select rightmost entry
    date = date.split("-")[-1]
    # Some weired year entries contain non-numeral characters, remove them
    date = re.sub('[^0-9]','', date)
    # Check that the year is within the range of retrieval, otherwise flag with year=0000
    if date not in yearlist:
        date = '0000'
    # Add month & day to make it SQL-date compatible
    date = date + '-00-00'
    return date

def sanitize_name(name):
    name = name.strip()
    name = name.strip(',')
    name = name.strip('.')
    if re.search('[\s\.]\w$', name):
        name += '.'
    return name

# This function takes a chunk of 200 bibliographical entries as a text  and looks for
# the AU, TI, etc. and puts them into a list; field can be ID, AU, T1, SN, PY, UR
def extract(text, field):
    element = text.split('{0}  - '.format(field))
    if len(element) > 1:
        element.pop(0)
        result = []
        for e in element:
            result += [e.split('\n', 1)]
        if (field == 'PY'):
            date = sanitize_year(result[0][0])
        if (field == 'AU'):
            author = sanitize_name(result[0][0])
        return result
    else:
        #print('unknown')
        return [['unknown']]

def slowdown(multiplier):
    all = 4
    i = abs(random.gauss(5, 2)/5*float(multiplier)*all)
    time.sleep(i)

# Initialize the logfiles for debugging
def initialize_logfiles():
    record = open(detailed_logfilepath,"w")
    record.write('<html>\n<head>\n<title>Detailed logfile - Melinda - {0} - {1}</title>\n<meta charset="UTF-8"></head>\n<body>\n'.format(date, zeit))
    record.close()
    record2 = open(short_logfilepath,"w")
    record2.write('<html>\n<head>\n<title>Short logfile - Melinda - {0} - {1}</title>\n<meta charset="UTF-8"></head>\n<body>\n'.format(date, zeit))
    record2.close()

# Finalize the logfiles for debugging
def finalize_logfiles():
    record = open(detailed_logfilepath,"a")
    record2 = open(short_logfilepath,"a")
    elapsed_time_seconds = time.time()-startzeit
    if elapsed_time_seconds > 100:
        zeit_string = str(round((elapsed_time_seconds/60))) + ' minutes'
    else:
        zeit_string = str(round(elapsed_time_seconds)) + ' seconds'
    stat_string = '\n' + str(total_record_count) + ' records retrieved from Melinda.<br>\n' + str(written_to_database_count) + ' records put to the local SQL database (table: theses).<br>\n'
    stat_string += str(planned_requests) + ' requests should have been made to Melinda.<br\n' + str(sent_requests_count) + ' requests made to Melinda.<br>\n'
    stat_string += 'Script execution took ' + zeit_string + '.\n'
    stat_string += "</body>\n</html>\n"
    print(stat_string)
    record.write(stat_string)
    record2.write(stat_string)
    record.close()
    record2.close()

# Returns the time since beginning of the script in minutes, the progress (how many of the total requests have been performed),
# and the estimated reminaing time
def progress():
    elapsed_time_seconds = time.time()-startzeit
    elapsed_time_minutes = elapsed_time_seconds/60
    if sent_requests_count > 20:
        # Estimate of total time
        ETA = planned_requests * elapsed_time_minutes / sent_requests_count
        # Estimate of remaining time
        remaining_time_minutes = str(round((ETA - elapsed_time_minutes), 1))
    else:
        remaining_time_minutes = 'still estimating... '
    return str(round(elapsed_time_minutes, 1)) + ' min (' + str(sent_requests_count) + ' of ' + str(planned_requests) + ' requests, ' + remaining_time_minutes + ' min remaining)'

def searchloop(position, university_searchterm_list, yearlist, langlist):
    global dosearch, sent_requests_count, total_record_count, previous_total_record_count, written_to_database_count
    # Start iterating from the position that is specified by the position list (default 0, 0, 0 = beginning)
    # Since the values of the position are changed when the search is started anywhere else except the
    # beginning, the function must remember the original position (probably not true!!!)
    original_positon = position
    for u_count in range (position[0], len(university_searchterm_list)):
        slowdown(slowdown_rate/3)
        for y_count in range (position[1], len(yearlist)):
            slowdown(slowdown_rate/5)
            for l_count in range (position[2], len(langlist)):
                slowdown(slowdown_rate/20)
                # New request
                # SEARCH TERMS
                # University is searched for with WRD (consecutive word search)
                # "theses" term is search for with WDI ()
                # SEARCH FILTERS
                # Language is filtered for with filter_code1 WLA
                # Year is filtered for with filter_code2 WYR
                # There might be wrong entries if e.g. the search term "University of Helsinki" appears in a dissertaton, but is e.g. part of the dissertations title
                # There might be missing entries if WRD doesn't retrieve all. Below the numbers of alternative retrievals
                # WTI = (University of Helsinki) AND SGN = väitösk  243
                # WRD = (University of Helsinki) AND SGN = väitösk  1765
                # WAU = (University of Helsinki) AND SGN = väitösk  13
                # WPU = (University of Helsinki) AND SGN = väitösk  1115
                #
                # This url stopped working sometime in 2016
                #url = "http://melinda.kansalliskirjasto.fi/F/?func=find-c&ccl_term={0}+AND+{1}&adjacent=N&x=0&y=0&filter_code_1=WLA&filter_request_1={2}&filter_code_2=WYR&filter_request_2={3}&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=".format(university[0], pubtype, language, year)
				# This is the new working search term:
                #url = "http://melinda.kansalliskirjasto.fi/F/?func=find-c&ccl_term=(WRD = (University of Helsinki) OR WRD = (Helsingin Yliopisto) OR WRD = (Helsingfors Universitet)) AND (WDI = diss OR WDI = V%C3%A4it%C3%B6skirja OR WDI = v%C3%A4it%C3%B6sk OR WDI = (Akademisk avhandling) OR WDI = (akad avh))&adjacent=Y&x=0&y=0&filter_code_1=WLA&filter_request_1=ENG&filter_code_2=WYR&filter_request_2=2015&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4="
                # final search term
                #print(university_searchterm_list[u_count][0])
                #print(l_count)
                #print(langlist[l_count])
                #print(yearlist[y_count])
                url = "http://melinda.kansalliskirjasto.fi/F/?func=find-c&ccl_term={0} AND (WDI = {1} OR WDI = {2} OR WDI = {3} OR WDI = {4} OR WDI = {5})&adjacent=Y&x=0&y=0&filter_code_1=WLA&filter_request_1={6}&filter_code_2=WYR&filter_request_2={7}&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=".format(university_searchterm_list[u_count][0], pubtype[0], pubtype[1], pubtype[2], pubtype[3], pubtype[4], langlist[l_count], yearlist[y_count])
                # Write individual search request to the logfile
                logfile('write_to_short_logfile', '<br>\n', progress(), "{0}, {1}, {2}".format(u_count, y_count, l_count))
                #tmp = "{0}, {1}, {2}".format(university_searchterm_list[u_count][1], yearlist[y_count], langlist[l_count])
                logfile('write_to_short_logfile', "{0}, {1}, {2}".format(university_searchterm_list[u_count][1], yearlist[y_count], langlist[l_count]))
                logfile('write_to_short_logfile', url)
                # Try to connect
                try:
                    r = requests.get(url)
                    sent_requests_count += 1
                    text = r.text
                    # The following line (checking for the absence of returned results) was replaced by checking that at least one result was returned
                    #if 'Hakusi ei tuottanut tulosta. Tarkista hakusanat.' not in text:
                    if 'Viitteet <span id="first">' in text:
                    # Get session id
                        id_string = find_next_occurence(text, 'URL=/F/', '-')
                        logfile('Session id: ', id_string)
                        text = substring_after(text, id_string)

                        # Get number of returned items
                        #print(text)
                        max_item = find_next_occurence(text, '</span> (yhteens', ')')
                        #print('Max item:', max_item)
                        max_item = max_item[-6:]
                        logfile('Max item:', max_item)
                        max_item = int(max_item)

                        #for i in range (1,int(max_item)+1):
                        ##for i in range (1, 2):
                        #    slowdown(0.2)
                        #    url = 'http://melinda.kansalliskirjasto.fi/F/' + id_string + '-17715?func=short-select-single&XXX' +'{0:06d}'.format(i) + '=on'
                        #    logfile(url)
                        #    r =  requests.get(url)
                        #url = 'http://melinda.kansalliskirjasto.fi/viitteet/ref.pl?sessionID=' + id_string + '-17715&func=short-mail&records=SELECT&range=++++++++1-+++++++10&exportType=ris&mail=0&address='

                        # Get the RIS data in chunks of chunksize (~250 seems to be the maximum the server can take)
                        text = ''
                        chunksize = 200
                        for i in range(chunksize,max_item,chunksize):
                            slowdown(20)
                            start = i-chunksize+1
                            end = i
                            starts = str(start).rjust(4, '+')
                            ends = str(end).rjust(4, '+')
                            url = 'http://melinda.kansalliskirjasto.fi/viitteet/ref.pl?sessionID=' + id_string + '-17715&func=short-mail&records=RANGE&range=+++++' + starts + '-+++++' + ends + '&exportType=ris&mail=0&address='
                            logfile(url)
                            r = requests.get(url)
                            text += '<h1 style="color:red">SECTION START' + str(start) + '-' + str(end) + '</h1>'
                            text += r.text
                        # One more round to get the leftovers
                        start = max_item - (max_item % chunksize) + 1
                        end = max_item
                        starts = str(start)
                        ends = str(end)
                        url = 'http://melinda.kansalliskirjasto.fi/viitteet/ref.pl?sessionID=' + id_string + '-17715&func=short-mail&records=RANGE&range=+++++' + starts + '-+++++' + ends + '&exportType=ris&mail=0&address='
                        logfile(url)
                        r = requests.get(url)
                        text += '<h1 style="color:red">SECTION START' + str(start) + '-' + str(end) + '</h1>'
                        text += r.text
                        #logfile('<pre>', text, '</pre>')
                        text = text.split('ER  - \n')
                        text.pop()
                        # How many records are following
                        logfile(str(len(text)))
                        i = 1
                        for element in text:
                            # Prints the whole record that is going to be parsed
                            logfile(str(i) + '. : ' + element, university_searchterm_list[u_count][1], str(yearlist[y_count]), langlist[l_count])
                            melinda_id = extract(element, 'ID')[0][0]
                            author = extract(element, 'AU')[0][0]
                            title = extract(element, 'T1')[0][0]
                            issn = extract(element, 'SN')[0][0]
                            date = extract(element, 'PY')[0][0]
                            url = extract(element, 'UR')
                            # Remove all URLs from the url list, that start with "http://linda"
                            for element in enumerate(url):
                                if element[:12] == "http://linda":
                                    url.pop(0)
                            if len(url) > 0:
                                url = url[0][0]
                            else:
                                url = 'NULL'
                            logfile("EXTRACTED DATA " +  str(i) + ": melinda_id: " + str(melinda_id) + ", author: " + author + ", title: " + title + ", issn: " + issn + ", date: " + date + ", url: ", url)
                            i += 1
                            total_record_count += 1
                            # Check whether the record is already in the local SQL database
                            query = "SELECT melinda_id, author, title, issn, date, url, university, language FROM theses WHERE melinda_id = %s OR title = %s"
                            logfile("\nQuery:", query, "melinda_id=" + melinda_id, "title=" + title, "\n")
                            try:
                                cursor.execute(query, (melinda_id, title))
                                rows = cursor.fetchall()
                                if len(rows) == 0:
                                    tmp = 'New record: ' + str(written_to_database_count) + ' of total ' + str(total_record_count) + ' retrieved records.'
                                    logfile(tmp)
                                    query = "INSERT INTO theses (melinda_id, author, title, issn, date, url, university, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                    #query = "INSERT INTO theses (melinda_id, author, title, issn, date, url, university, language) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})".format(melinda_id, author, title, issn, date, url, university[1], language)
                                    logfile(query, "melinda_id=" + melinda_id, "author=" + author, "title=" + title, "issn=" + issn, "date=" + date, "url=" + url, "unversity=" + university_searchterm_list[u_count][1], "language=" + langlist[l_count])
                                    try:
                                        cursor.execute(query, (melinda_id, author, title, issn, date, url, university_searchterm_list[u_count][1], langlist[l_count]))
                                        #cursor.execute(query)
                                        sqlcon.commit()
                                        written_to_database_count += 1
                                    except phddb.Error as e:
                                        if e[0]!= '':
                                            print(query)
                                            raise
                                    # This slowdown is only necessary if you ant to watch the progress
                                    #slowdown(1)
                                if len(rows) == 1:
                                    if melinda_id == rows[0][0]:
                                        logfile('Already a record with the id {0} in the local SQL database (theses table)!'.format(rows[0][0]))
                                    else:
                                        if (author == rows[0][1]) and (title == rows[0][2]) and (date == rows[0][4]):
                                            logfile('Already a record with the same title/author/year combination in the local SQL database (table theses)! Merging...'.format(rows[0][0]))
                                            # If the exisiting record (which has the same author, title and year) doesn't have university, issn or url set, add this data now!
                                            query = "UPDATE theses set "
                                            update = 'no'
                                            if rows[0][6] == '':
                                                new_university = university_searchterm_list[u_list][1]
                                                update = 'yes'
                                                query += "university = '{0}', ".format(new_university)
                                            if rows[0][3] == '':
                                                new_issn = issn
                                                update = 'yes'
                                                query += "issn = '{0}', ".format(new_issn)
                                            if rows[0][5] == '':
                                                new_url = url
                                                update = 'yes'
                                                query += "url = '{0}', ".format(new_url)
                                            if update == 'yes':
                                                query = query[:-2]
                                                logfile(query)
                                                try:
                                                    cursor.execute(query)
                                                    sqlcon.commit()
                                                    written_to_database_count += 1
                                                except phddb.Error as e:
                                                    if e[0]!= '':
                                                        print(query)
                                                        raise
                                            else:
                                                print("No new information. No update query issued.")
                                        else:
                                            logfile('Same title, but different year or author. This should be almost impossible!')
                                    #time.sleep(3)
                                else:
                                    logfile("Already more than 2 records with the same title/author/year combination in the local SQL database (table theses). This should not be possible!")
                            except phddb.Error as e:
                                logfile('write_to_short_logfile', '\n\nError with inserting new records into database: \n', str(e))
                                return
                            logfile('\n')
                        logfile('write_to_short_logfile', 'This request returned ' + str(total_record_count - previous_total_record_count) + ' records, inserted: ' + str(written_to_database_count) + ', total: ' + str(total_record_count))
                    else:
                        logfile('write_to_short_logfile', 'This request did not return any records' + ', total: ' + str(total_record_count))
                        # Wait between requesting the same data with a different language filter
                        slowdown(2)
                    previous_total_record_count = total_record_count
                except requests.exceptions.Timeout as e:
                    # Maybe set up for a retry, or continue in a retry loop
                    print(str(e))
                    logfile('write_to_short_logfile', '\n\nError: \n', str(e))
                    slowdown(200)
                    return [u_count, y_count, l_count]
                except requests.exceptions.TooManyRedirects as e:
                    # Tell the user their URL was bad and try a different one
                    print(str(e))
                    logfile('write_to_short_logfile', '\n\nError: \n', str(e))
                    slowdown(200)
                    return [u_count, y_count, l_count]
                except requests.exceptions.RequestException as e:
                    # catastrophic error. bail.
                    print(str(e))
                    logfile('write_to_short_logfile', '\n\nError: \n', str(e))
                    slowdown(200)
                    return [u_count, y_count, l_count]
            position[2] = 0
        position[1] = 0
    # Check whether the end of the search has been reached
    # 1 needes to be added to u_count, y_count and l_count in order for the
    # search to stop correctly. E.g. for a list contaning 16 universities, 38 years and
    # 13 languages, the last search is 15-37-12
    if ([len(university_searchterm_list), len(yearlist), len(langlist)] == [u_count+1, y_count+1, l_count+1]):
        dosearch = False
    return [u_count, y_count, l_count]

# Connection credentials
sqlhost = 'localhost'
sqllogin = 'phddb_user'
sqlpassword = 'zdshDc6UZXnjUap6' #This needs to be changed if you want to be secure
sqldb = 'phddb'

# Get command line parameter to regulate the speed with which the requests are made
# to the library server. 50 is ok, but occasionlly results in being blocked. For
# unattended runs, use 200
try:
    slowdown_rate = int((sys.argv[1]))
except Exception as e:
    slowdown_rate = 50

# Logfile names & location
date = time.strftime("%Y-%m-%d")
zeit = time.strftime("%H-%M-%S")
startzeit = time.time()
# Create the logfiles directory if it doesn't already exist
os.makedirs("logfiles",exist_ok=True)
detailed_logfilepath = "logfiles/logfile_{0}_{1}.html".format(date, zeit)
short_logfilepath = "logfiles/logfile_{0}_{1}_short.html".format(date, zeit)

# Create connection
sqlcon = phddb.connect(host=sqlhost, user=sqllogin, passwd=sqlpassword, db=sqldb, charset='utf8')
initialize_logfiles()

with sqlcon:
    cursor = sqlcon.cursor()

    # Write preamble
    cursor.execute("SELECT VERSION()")
    ver = 'Database version: ' + str(cursor.fetchone())
    logfile('write_to_short_logfile', ver)
    cursor.execute("SELECT COUNT(*) FROM theses")
    ver ='Database \'theses\' contains: ' + str(cursor.fetchone()) + ' entries\n'
    logfile('write_to_short_logfile', ver)

    # Dissertations
    pubtype = ['diss', 'v%25C3%25A4it%25C3%25B6sk', '(akad avh)', 'V%C3%A4it%C3%B6skirja', '(Akademisk avhandling)']
    # langlist has 13 entries
    langlist = ['ENG', 'FIN', 'SWE', 'SPA', 'ITA', 'NOR', 'FRE', 'SMI', 'GER', 'DAN', 'RUS', 'EST', 'HUN']
    # 16 Universities: UEF, Kuopio and Joensuu are listed separately (effectively 14 universities)
    # AU: Aalto-yliopiston kauppakorkeakoulu; Aalto-universitets handelshögskola; Helsinki School of Economics (HSE); Helsinki School of Economics and Business Administration (HSEBA); Aalto University School of Economics; Aalto-yliopiston taiteiden ja suunnittelun korkeakoulu; Aalto-universitetets högskola för konst, design och arkitektur
    universities = [['University of Helsinki', 'Helsingin Yliopisto', 'Helsingfors Universitet', 'UH'],
                    ['University of Turku', 'Turun Yliopisto', 'Åbo Universitet', 'UTU'],
                    ['Aalto University', 'Aalto-yliopisto', 'Aalto-universitetet', 'Helsinki University of Technology', 'Helsinki School of Economics', 'University of Art and Design Helsinki', 'Teknillinen korkeakoulu', 'Tekniska högskolan', 'AU'],
                    ['Åbo Akademi University', 'Åbo Akademi', 'AA'],
                    ['Hanken School of Economics', 'Svenska handelshögskolan', 'Hanken svenska handelshögskolan', 'HAN'],
                    ['University of Eastern Finland', 'Itä-Suomen yliopisto', 'Östra Finlands universitet', 'UEF'],
                    ['Lappeenranta University of Technology', 'Lappeenrannan teknillinen yliopisto', 'Villmanstrands tekniska universitet', 'Lappeenrannan teknillinen korkeakoulu', 'LUT'],
                    ['Tampere University of Technology', 'Tampereen teknillinen yliopisto', 'Tammerfors tekniska universitet', 'Tampereen teknillinen korkeakoulu', 'TUT'],
                    ['University of Jyväskylä', 'Jyväskylän yliopisto', 'Jyväskylä universitet', 'JyU'],
                    ['University of Lapland', 'Lapin yliopisto', 'Lapplands universitet', 'LY'],
                    ['University of Tampere', 'Tampereen yliopisto', 'Tampere universitet', 'TU'],
                    ['University of Oulu', 'Oulun yliopisto', 'Oulu universitet', 'OU'],
                    ['University of Vaasa', 'Vaasan yliopisto', 'Vaasa universitet', 'Vaasan korkeakoulu', 'VU'],
                    ['University of the Arts Helsinki', 'Taide-yliopisto', 'Konst-universitetet', 'Helsinki Theatre Academy', 'Helsinki Kuvataideakatemia', 'Helsinki Teatterikorkeakoulu', 'Helsinki Sibelius-Akatemia', 'UAH'],
                    ['University of Kuopio', 'Kuopion yliopisto', 'Kuopio universitet', 'KuU'],
                    ['University of Joensuu', 'Joensuun yliopisto', 'Joensuu universitet', 'Joensuun korkeakoulu', 'JoU']]
    # This determines the years for which theses are retrieved
    # yearlist has 38 entries (Python doesn't include the end of a range, in order to include 2017 theses, you need to specify 2018 as the end of the range)
    yearlist = list(range(1980,2018))
    # The position[] list keeps track of the position in the work list (what university, what year, what language)
    # If you want to continue a script from a specific place in the work list, you can set it here
    # in the order: university, year, language
    position = [0, 0, 0]
    # Override default lists
    # This e.g. starts the script from UH, 2003, HUN
    #position = [0, 23, 12]
    # This e.g. starts the script from UTU, 1995, ENG
    #position = [1, 15, 0]
    # This limits the search to a specific language
    #langlist = ['SWE']
    #langlist = ['ENG']
    # This limits the search to a specific set of universities
    #universities = [['University of Helsinki', 'Helsingin Yliopisto', 'Helsingfors Universitet', 'UH']]
    # This limits the search to certain year(s)
    #yearlist = [2011, 2012, 2013, 2014, 2015]
    #yearlist = [2015]

    # How many requests are scheduled? Total amount is 13 * 16 * 38 = 7904
    # planned_requests = len(university_searchterm_list)*len(yearlist)*len(langlist)
    # If not starting at 0,0,0, calculate how many requests need to be done
    planned_requests = (len(universities) - position[0] - 1) * len(yearlist) * len(langlist) + (len(yearlist) - position[1] - 1) * len(langlist) + (len(langlist) - position[2])
    logfile('write_to_short_logfile', str(len(universities)), str(len(yearlist)), str(len(langlist)))
    # The scraper should be executed in regular intervals (e.g once per day) to insert the new theses
    # The current year should bee the only list element in yearlist
    current_year = time.strftime("%Y")
    #yearlist = [int(current_year)]
    logfile('write_to_short_logfile', '<br>\nUniversities to search:\n', universities, '\n')
    logfile('write_to_short_logfile', 'Years to search:\n', yearlist, '\n')
    logfile('write_to_short_logfile', 'Languages to search:\n', langlist, '\n')
    logfile('write_to_short_logfile', 'Starting position:\n', str(position[0]) + ' = ' + str(universities[position[0]]), str(position[1]) + ' = ' + str(yearlist[position[1]]), str(position[2]) + ' = ' + str(langlist[position[2]]), '\n')
    logfile('write_to_short_logfile', 'Number of requests remaining:\n', str(planned_requests), '\n')

    # Create search terms for universities
    universities = [[x.replace(' ', '+') for x in l] for l in universities]
    i = 1
    university_searchterm_list = []
    for l in universities:
        #print(l, '\n')
        acronym = l.pop()
        #print(acronym, '\n')
        #print(l, '\n')
        concat = '%29+OR+WRD+%3D+%28'.join(l)
        #print(concat, '\n')
        concat = "%28WRD+%3D+%28" + concat + '%29%29';
        #print(concat, '\n')
        tmp = [concat, acronym]
        university_searchterm_list.append(tmp)
        #print(str(i),' university_searchterm_list:', university_searchterm_list, '\n')
        i += 1
    logfile('write_to_short_logfile', 'university_searchterm_list:', university_searchterm_list, '\n')

    # Reset session
    url = 'http://melinda.kansalliskirjasto.fi/F/?func=logout&local_base=fin01&con_lng=fin'
    r = requests.get(url)
    # Count all records
    total_record_count = 0
    # Keep the previous total record count to calculate how many new records have been retrieved
    previous_total_record_count = 0
    # Count all records that have beeen put into the local database
    written_to_database_count = 0
    # Count all requests sent to Melinda
    sent_requests_count = 0

    # Each loop tries to retrive all records. If the retrieval is interrupted (connection error),
    # the position in the search is returned and the loop is restarted with the new position as
    # the starting position. If the loop is exited without error and the search positon is
    # equal to the target, the search variable is set to False and the program exists.
    dosearch = True
    search_cycle_number = 0
    while dosearch == True:
        search_cycle_number += 1
        logfile('write_to_short_logfile', "Cycle number " + str(search_cycle_number) + ", resume position: " + str(position))
        position = searchloop(position, university_searchterm_list, yearlist, langlist)
        if dosearch == True:
            slowdown(slowdown_rate)
        else:
            logfile('write_to_short_logfile', 'The script was executed until the following position in the worklist: ' + str(position[0]) + '-' + str(position[1]) + '-' + str(position[2]))
    cursor.close()
finalize_logfiles()
