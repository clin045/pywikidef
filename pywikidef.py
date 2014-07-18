from bs4 import BeautifulSoup
import os
import urllib.request
import argparse
import random

debug = False

def getParagraphs(content, amount):
	""" Grab all paragraph elements from content 

		content = list of html elements 
		outputs the list of paragraphs """

	global debug

	paragraphs = []
	#Used to keep track of how many paragraphs we have
	used = 0
	for item in content:
		# If the wiki page is one of those may refer to pages
		if item.find(' may refer to:') > -1 or item.find(' may also refer to:') > -1:
			paragraphs.append(checkMultipleOptions(content))
			break
		# None of those silly single line blank paragraphs
		if len(item) < 10:
			continue
		# Grabs the paragraphs that aren't massive divs in disguise
		if item.find('<p>') > -1 and item.find('<div>')  == -1 and item.find('<table') == -1:
			if item.find('For search options') > -1: paragraphs.append("That item could not be found, try searching something different")
			else: paragraphs.append(item)
			used += 1
		if used >= amount:
			break
	if debug: print("Got that info")
	return paragraphs

def checkExactTerm(soup):
	""" Defaults to first link in searches

		soup = the html of the current webpage in soup form
		outputs the new webpage in soup form """

	# mw-search-result-heading is used for the body of the links to the search results - grabs the first link
	firstLink = soup.find("div", { "class" : "mw-search-result-heading" })
	if firstLink:
		# Open the first link and get the html to return
		site = urllib.request.urlopen('http://en.wikipedia.org'+firstLink.a.get('href'))
		soup = BeautifulSoup(site)
		soup.prettify()
	return soup	

def checkMultipleOptions(content):
	""" Print list of links for available pages for a search

		content = list of html elements 
		outputs a list of lists """

	paragraphs = ""
	paragraphs += "<p>There were multiple things found for that item</p>"
	for item in content:
		#Get the lists of links provided by the page
		if item.find('<ul>') > -1 and item.find('class="toc"') == -1:
			paragraphs += str(item)
	return paragraphs

def getUrlSoup(search):
	""" Gets the soup form of the webpage

		search = the item they want 
		ouputs the html in soup form """

	# Opens the url based on the search term and returns the html
	searchurl = 'http://en.wikipedia.org/w/index.php?search=' + search + '&title=Special%3ASearch&go=Go'
	site = urllib.request.urlopen(searchurl)
	soup = BeautifulSoup(site)
	soup.prettify()
	return soup

def getInformation(search, amount):
	""" Main method for getting the term information

		search = the search term
		amount = the amount of paragraphs to find
		outputs a list of lists of items """

	# Get the URL's html
	soup = getUrlSoup(search)
	# Check if the term was searched or if it's actually a page
	soup = checkExactTerm(soup)
	# Grab the content pane's children for checking
	content = map(str, soup.find('div', { 'id' : 'mw-content-text'}).children)
	# Grab the amount of paragraphs needed and return
	return getParagraphs(content, amount)

def outputToHTML(searchTerms, termParagraphs, outputFile):
	""" Ouputs the information in HTML format

		searchTerms = list of items
		termParagraphs = output from getInformation()
		outputFile = the file path to output """

	global debug

	if len(searchTerms) == 0 or len(termParagraphs) == 0:
		print("No output")
		return
	# We don't like \ slashes
	outputFile.replace('\\', '/')
	#encoding needed for unicode character shenanigans when writing to the file.
	html = open(outputFile, 'w', encoding="utf-8-sig")
	# TODO - use a template and make it pretty
	# Writes it to a really plain html file. Inline styling is the best
	html.write('<html>')
	html.write('<h1>~Report~</h1>')
	for search in searchTerms:
		html.write('<ul style="list-style-type:none">')
		html.write('<li><a href="#'+search+'">' + search + '</a></li>')
		html.write('</ul>')
	for index, term in enumerate(termParagraphs):
		html.write('<h3 style="background-color:#ccc;" id="'+searchTerms[index]+'">'+searchTerms[index].replace('+',' ')+'</h3>')
		for para in term:
			try:
				para = para.replace('href="', 'href="http://en.wikipedia.org')
				html.write(str(para))
			except UnicodeEncodeError:
				html.write("Unicode issues outputting this paragraph")
		if debug: print("Output information for " + searchTerms[index])
	html.write('</html>')
	print("Ouput to file: " + outputFile)

def readInfile(inputFile):
	""" Inputs the search terms from a file 

		inputFile = the path to the file
		outputs the list of lines """

	global debug

	# Still don't like \ slashes
	inputFile.replace("\\","/")
	f = open(inputFile,'r')
	lines = f.readlines()
	for l in range(0,len(lines)):
		# Put the terms in the correct search format (no spaces or \n)
		lines[l]=lines[l].replace(' ','+')
		lines[l]=lines[l].replace('\n','')
	f.close()
	if debug: print("Finished getting input from file")
	return lines

def searchMode(amount):
	""" Loop for 1 word per lookup searching 

		amount = # of paragraphs to get 
		returns a list of lists of paragraphs 
		returns the terms searched """

	global debug

	Paragraphs = []
	searchTerms = []
	searchTerm = input("What would you like to search?\nquit() for quit\n")
	# Go until they type quit()
	while searchTerm != 'quit()':
		# Add what they searched to the search terms
		searchTerms.append(searchTerm.replace(' ', '+'))
		# Get the info and add it to termParagraphs in paragraph format
		termParagraphs = [getInformation(searchTerm, amount)]
		# Temp var to hold the paragraphs
		temp = []
		for index, term in enumerate(termParagraphs):
			for para in term:
				temp.append(para)
		# Add the list to the list of lists to return later
		Paragraphs.append(temp)
		if debug: input("Enter to continue")
		#Go again!
		searchTerm = input("\n"*100 + "What would you like to search?\nquit() for quit\n")
	return Paragraphs, searchTerms

def main():
	""" Main method """

	global debug

	# Parser for command line arguments
	parser = argparse.ArgumentParser(prog="pywikidef",description="pywikidef") 
	parser.add_argument('--inputfile','-i', dest='inputFile', help='Input file with list of searchTerms')
	parser.add_argument('--output', '-o', dest='outputFile', help='Output File', default="terms.html")
	parser.add_argument('--amount', '-a', dest='amount', default=1, help='Amount of paragraphs')
	parser.add_argument('--search', '-s', action='store_true', help='Enter 1 term at a time searching')
	parser.add_argument('--flashlight', '-f', action='store_true', help='TURN DOWN FOR WHAT')
	parser.add_argument('--debug', '-d', action='store_true', help='Enable debugging')
	args = parser.parse_args()
	debug = args.debug
	if args.flashlight:
		while True:
			os.system("color " + str(random.randrange(0, 9)) + str(random.randrange(0, 9)))
			os.system("echo PARTY TIME")
	amount = int(args.amount)
	if args.inputFile:
		searchTerms = readInfile(args.inputFile)
		termParagraphs = []
		for t in searchTerms:
			if debug: print("Getting information for " + t)
			termParagraphs.append(getInformation(t, amount))
		outputToHTML(searchTerms, termParagraphs, args.outputFile)
	elif args.search:
		termParagraphs, searchTerms = searchMode(amount)
		outputToHTML(searchTerms, termParagraphs, args.outputFile)
	else:
		parser.print_help()

if __name__ == '__main__':
	main()