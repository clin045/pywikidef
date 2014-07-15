from bs4 import BeautifulSoup
import sys
import io
import urllib.request
import argparse

def getParagraphs(content):
	""" Grab all paragraph elements from content 

		content = list of html elements 
		outputs the list of paragraphs """

	paragraphs = []
	for item in content:
		# If the wiki page is one of those may refer to pages
		if item.find(' may refer to:') > -1:
			paragraphs = checkMultipleOptions(content)
			break
		# None of those silly single line blank paragraphs
		if len(item) < 10:
			continue
		# Grabs the paragraphs that aren't massive divs in disguise
		if item.find('<p>') > -1 and item.find('<div>')  == -1:
			paragraphs.append(item)
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

	paragraphs = []
	paragraphs.append("<p>There were multiple things found for that item so here's a link or two since I can't read minds")
	for item in content:
		#Get the lists of links provided by the page
		if item.find('<ul>') > -1:
			paragraphs.append(item)
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
	# Grab all of the content's paragraphs
	paragraphs = getParagraphs(content)
	# Group them correctly for html output
	output = []
	for index in range(amount):
		try:
			output.append(paragraphs[index])
		except IndexError:
			print("\n\nThere were only " + str(index) + " paragraphs for the search: " + search)
			break
	return output

def outputToHTML(searchTerms, termParagraphs, outputFile):
	""" Ouputs the information in HTML format

		searchTerms = list of items
		termParagraphs = output from getInformation()
		outputFile = the file path to output """

	# We don't like \ slashes
	outputFile.replace('\\', '/')
	html = open(outputFile, 'w')
	# TODO - use a template and make it pretty
	# Writes it to a really plain html file
	html.write('<html>')
	for index, term in enumerate(termParagraphs):
		html.write("<p>-----------------"+searchTerms[index].replace("+"," ")+"-----------------</p>")
		for para in term:
			para = para.replace('href="', 'href="http://en.wikipedia.org')
			html.write(str(para))
	html.write('</html>')
	print("Ouput to file: " + outputFile)

def readInfile(inputFile):
	""" Inputs the search terms from a file 

		inputFile = the path to the file
		outputs the list of lines """

	# Still don't like \ slashes
	inputFile.replace("\\","/")
	f = open(inputFile,'r')
	lines = f.readlines()
	for l in range(0,len(lines)):
		# Put the terms in the correct search format (no spaces or \n)
		lines[l]=lines[l].replace(' ','+')
		lines[l]=lines[l].replace('\n','')
	f.close()
	return lines

def main():
	""" Main method """

	# Correct encoding for output whenever I get around to doing single search terms
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')
	# Parser for command line arguments
	parser = argparse.ArgumentParser(prog="pywikidef",description="pywikidef") 
	parser.add_argument('--inputfile','-i',dest='inputFile', help='Input file with list of searchTerms')
	parser.add_argument('--output', '-o', dest='outputFile', help='Output File')
	parser.add_argument('--amount', '-a', dest='amount', default=1, help='Amount of paragraphs')
	#TODO - single search terms
	args = parser.parse_args()
	amount = int(args.amount)
	outputFile = args.outputFile
	inputFile = args.inputFile
	if inputFile:
		searchTerms = readInfile(inputFile)
		termParagraphs = []
		for t in searchTerms:
			termParagraphs.append(getInformation(t, amount))
		outputToHTML(searchTerms, termParagraphs, outputFile)
	else:
		print(args.help)

if __name__ == '__main__':
	main()