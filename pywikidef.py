from bs4 import BeautifulSoup
import sys
import io
import urllib.request
import argparse

def getWebsite(search, amount):
	url = 'http://en.wikipedia.org/wiki/' + search.replace(" ", "_")
	site = urllib.request.urlopen(url)
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
			html.write(str(para))
	html.write('</html>')

def readInfile(inp):
	inp.replace("\\","/")
	f = open(inp,'r')
	lines = f.readlines()
	for l in range(0,len(lines)):
		lines[l]=lines[l].replace(' ','_')
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
	outputFile = args.outputFile.replace('\\', '/')
	inf = args.inf.replace('\\', '/')
	if(search):
		#TODO get a single term and print to console 
	if(inf):
		terms = readInfile(inf)
		termParas = []
		for t in terms:
			termParas.append(getWebsite(t, amount))
		outputToHTML(termParas, outputFile)

		
if __name__ == '__main__':
	main()
