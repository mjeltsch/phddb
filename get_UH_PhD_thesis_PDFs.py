#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, urllib3, shutil

# Create a dictionnary for the numerical values of PhD thesis collections
facultydict = {'18063': 'Biological and Environmental Sciences', '18064': 'Veterinary Medicine', '18065': 'Pharmacy', '18066': 'Arts', '18067': 'Behavioural Sciences', '18068': 'Medicine', '18069': 'Agriculture and Forestry', '18070': 'Science', '18071': 'Law', '18072': 'Theology', '18073': 'Social Sciences'}

# Try to make the "files" directory and a subdirectory for each faculty

if not os.path.exists("files"):
	os.makedirs("files")

for key, value in facultydict.items():
	path = "files/" + str(value)
	if not os.path.exists(path):
		os.makedirs(path)

counter_downloaded_PDF = 0 # counts all newly downloaded PDFs
counter_all_PDF = 0 # counts all PDFs
counter_faculty_PDF = 0 # counts newly downloaded PDF files for the individual faculty
counter_old_PDF = 0 # counts PDFs, that are already present on the local drive
counter_faculty_theses = 0 # Counts all theses that are in ethesis.helsinki.fi for that faculty
counter_all_theses = 0 # Counts all theses in ethesis.helsinki.fi

for key, value in facultydict.items():
	http = urllib3.PoolManager()
	url = "https://helda.helsinki.fi/handle/10138/" + key + "/browse?type=dateissued&sort_by=3&order=DESC&rpp=2000&offset=0"
	textstring = http.request('GET', url).data.decode('utf-8')
	for line in textstring.splitlines():
		# Count how many theses altogether (the number of items in the two lists "ds-artifact-item even" and "ds-artifact-item odd")
		if line == "<li class=\"ds-artifact-item odd\">":
			counter_faculty_theses += 1
		elif line == "<li class=\"ds-artifact-item even\">":
			counter_faculty_theses += 1
		#If the first 65 characters of a line match
		elif line[:65] == "<a alt=\"Download\" title=\"Download\" href=\"/bitstream/handle/10138/":
			variable_url_part = line.split('"')[5]
			# Generate a unique filename from number and filename on server
			#filename = "files/" + value + "/" + variable_url_part.split('/')[4] + "_" + variable_url_part.split('/')[5].split('?')[0]
			# Alternative, that puts all files into the same folder with numbers only
			filename = "files/" + variable_url_part.split('/')[4] + ".pdf"
			# Generate URL for the PDF
			PDFurl = "https://helda.helsinki.fi" + variable_url_part
			if not os.path.exists(filename):
				# Retrieve PDF file and save
				r = http.request('GET', PDFurl, preload_content=False)
				PDFfile = open(filename, 'wb')
				shutil.copyfileobj(r, PDFfile)
				PDFfile.close()
				counter_faculty_PDF +=1
			else:
				counter_old_PDF += 1
	print(str(counter_faculty_theses) + " theses are listed for the Faculty of " + value + " on ethesis.helsinki.fi.")
	print(str(counter_faculty_PDF) + " new PDF files were downloaded for the Faculty of " + value + ".")
	print(str(counter_old_PDF) + " old PDF were previosuly already downloadeded for the Faculty of " + value + ".")
	print(str(counter_faculty_PDF + counter_old_PDF) + " total PDFs for the Faculty of " + value + ".")
	percentage = (counter_faculty_PDF + counter_old_PDF)*100/counter_faculty_theses	
	print(str(round(percentage, 1)) + " % of theses in the Faculty of " + value + " have made the full text online available.\n")
	counter_downloaded_PDF += counter_faculty_PDF	
	counter_all_PDF += (counter_faculty_PDF + counter_old_PDF)
	counter_faculty_PDF = 0
	counter_old_PDF = 0
	counter_all_theses += counter_faculty_theses
	counter_faculty_theses = 0
print("\nTotal number of theses in ethesis.helsinki.fi: " + str(counter_all_theses) + ".")
print(str(round(counter_all_PDF*100/counter_all_theses, 1)) + "% of them have full text available online.")
print("Newly downloaded PDFs: " + str(counter_downloaded_PDF) + ".")
print("Altogether (downloaded + old): " + str(counter_all_PDF) + " PDF files.")

