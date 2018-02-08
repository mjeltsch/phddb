#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, urllib3, shutil, certifi

# Create a dictionnary for the numerical values of PhD thesis collections
facultylist = [['18063', 'Biological and Environmental Sciences'], ['18064', 'Veterinary Medicine'], ['18065', 'Pharmacy'], ['18066', 'Arts'], ['18067', 'Behavioural Sciences'], ['18068', 'Medicine'], ['18069', 'Agriculture and Forestry'], ['18070', 'Science'], ['18071', 'Law'], ['18072', 'Theology'], ['18073', 'Social Sciences']]

# Try to make the FILEDIR directory
FILEDIR = "files/pdf"
if not os.path.exists(FILEDIR):
	os.makedirs(FILEDIR)

# Counters for total
total_thesis_count = 0
total_file_count = 0
total_new_file_count = 0
total_old_file_count = 0
total_new_PDF_count = 0
total_new_nonPDF_count = 0

# Counters for individual faculties
faculty_thesis_count = 0
faculty_file_count = 0
faculty_new_file_count = 0
faculty_old_file_count = 0
faculty_new_PDF_count = 0
faculty_new_nonPDF_count = 0

previously_downloaded_file_list = []

for faculty in facultylist:
	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	# The first URL would be:
	# https://helda.helsinki.fi/handle/10138/18063/browse?type=dateissued&sort_by=3&order=DESC&rpp=2000&offset=0
	url = "https://helda.helsinki.fi/handle/10138/" + faculty[0] + "/browse?type=dateissued&sort_by=3&order=DESC&rpp=2000&offset=0"
	textstring = http.request('GET', url).data.decode('utf-8')
	print("\nDOWNLOADING THESES FROM THE FACULTY OF " + faculty[1].upper())
	print(url)
	for line in textstring.splitlines():
		#Count how many theses altogether INCLUDING THOISE WITHOUT DOWNLOAD (the number of items in the two lists "ds-artifact-item even" and "ds-artifact-item odd")
		if line == "<li class=\"ds-artifact-item odd\">":
			faculty_thesis_count += 1
		elif line == "<li class=\"ds-artifact-item even\">":
			faculty_thesis_count += 1
		#If the first 65 characters of a line match
		elif line[:65] == "<a alt=\"Download\" title=\"Download\" href=\"/bitstream/handle/10138/":
			print(".", end="")
			variable_url_part = line.split('"')[5]
			# Generate URL for the PDF
			PDFurl = "https://helda.helsinki.fi" + variable_url_part
			faculty_file_count +=1
			# Generate filenames to check whether the file was already downlaoded before
			filename = FILEDIR + "/" + variable_url_part.split('/')[4]
			PDF_filename =  filename + ".pdf"
			nonPDF_filename = filename + ".nonPDF"
			if (os.path.exists(PDF_filename) or os.path.exists(nonPDF_filename)):
				faculty_old_file_count += 1
				previously_downloaded_file_list.append(filename)
				print("\nPreviously downloaded: " + str(total_old_file_count + faculty_old_file_count) + ". " + filename.split('/')[2], end='')
			else:
				faculty_new_file_count += 1
				# Retrieve file
				r = http.request('GET', PDFurl, preload_content=False)
				# Save file only if it is a PDF
				if r.headers['Content-Type'] == 'application/pdf':
					# Generate a unique filename from number and filename on server
					filename = FILEDIR + "/" + variable_url_part.split('/')[4] + ".pdf"
					PDFfile = open(filename, 'wb')
					shutil.copyfileobj(r, PDFfile)
					PDFfile.close()
					faculty_new_PDF_count += 1
				else:
					# Generate a unique filename from number and filename on server
					filename = FILEDIR + "/" + variable_url_part.split('/')[4] + ".nonPDF"
					nonPDFfile = open(filename, 'wb')
					shutil.copyfileobj(r, nonPDFfile)
					nonPDFfile.close()
					faculty_new_nonPDF_count += 1

	faculty_percentage = faculty_file_count*100/faculty_thesis_count
	print("\nTotal number of theses for the Faculty of " + faculty[1] + ": " + str(faculty_thesis_count) + ".")
	print("Total number of theses in ethesis.helsinki.fi that have online files: " + str(faculty_file_count) + ".")
	print("Newly downloaded files: " + str(faculty_new_file_count) + ".")
	print("Newly downloaded PDFs: " + str(faculty_new_PDF_count) + ".")
	print("Newly downloaded non-PDFs: " + str(faculty_new_nonPDF_count) + ".")
	print(str(round(faculty_percentage, 1)) + " % of theses in the Faculty of " + faculty[1] + " have made files (full text) online available.\n")

	# Count totals by adding the numbers for individual faculties
	total_thesis_count += faculty_thesis_count
	total_file_count += faculty_file_count
	total_new_file_count += faculty_new_file_count
	total_old_file_count += faculty_old_file_count
	total_new_PDF_count += faculty_new_PDF_count
	total_new_nonPDF_count += faculty_new_nonPDF_count

	# Reset counters for individual faculties
	faculty_thesis_count = 0
	faculty_file_count = 0
	faculty_new_file_count = 0
	faculty_old_file_count = 0
	faculty_new_PDF_count = 0
	faculty_new_nonPDF_count = 0

total_percentage = total_file_count*100/total_thesis_count
print("\nTotal number of theses in ethesis.helsinki.fi: " + str(total_thesis_count) + ".")
print("Total number of theses in ethesis.helsinki.fi that have online files: " + str(total_file_count) + ".")
print("Newly downloaded files: " + str(total_new_file_count) + ".")
print("Newly downloaded PDFs: " + str(total_new_PDF_count) + ".")
print("Newly downloaded non-PDFs: " + str(total_new_nonPDF_count) + ".")
print(str(round(total_percentage, 1)) + " % of theses have made files (full text) online available.\n")
