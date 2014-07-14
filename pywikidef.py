from bs4 import BeautifulSoup
import sys
import io
import urllib.request
import argparse

def getWebsite(search, amount):
	searchurl = 'http://en.wikipedia.org/w/index.php?search=' + search + '&title=Special%3ASearch&go=Go'
	site = urllib.request.urlopen(searchurl)
	soup = BeautifulSoup(site)
	soup.prettify()
	firstLink = soup.find("div", { "class" : "mw-search-result-heading" })
	if firstLink:
		site = urllib.request.urlopen('http://en.wikipedia.org'+firstLink.a.get('href'))
		soup = BeautifulSoup(site)
		soup.prettify()
	paras = soup.find_all('p')
	output = []
	for index in range(amount):
		try:
			output.append(str(paras[index]))
		except IndexError:
			print("\n\nThere were only " + str(index) + " paragraphs")
			break
	return output

def outputToHTML(terms, outputFile):
	html = open(outputFile, 'w')
	html.write('<html>')
	for term in terms:
		for para in term:
			para = para.replace('href="', 'href="http://en.wikipedia.org')
			html.write(str(para))
	html.write('</html>')

def readInfile(inp):
	inp.replace("\\","/")
	f = open(inp,'r')
	lines = f.readlines()
	for l in range(0,len(lines)):
		lines[l]=lines[l].replace(' ','+')
		lines[l]=lines[l].replace('\n','')
	f.close()
	return lines

def main():
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')
	parser = argparse.ArgumentParser(prog="pywikidef",description="pywikidef") 
	parser.add_argument('--input', '-i', dest='search', help='Search a single term')
	parser.add_argument('--output', '-o', dest='outputFile', help='Output File')
	parser.add_argument('--inputfile','-if',dest='inf', help='Input file with list of terms')
	parser.add_argument('--amount', '-a', dest='amount', default=1, help='Amount of paragraphs')
	args = parser.parse_args()
	search = args.search
	amount = int(args.amount)
	outputFile = args.outputFile
	inf = args.inf
	if(search):
		#TODO get a single term and print to console 
		print('search')
	if(inf):
		terms = readInfile(inf.replace('\\', '/'))
		termParas = []
		for t in terms:
			termParas.append(getWebsite(t, amount))
		outputToHTML(termParas, outputFile.replace('\\', '/'))
		
if __name__ == '__main__':
	main()
