from bs4 import BeautifulSoup
import sys
import io
import urllib.request
import argparse

def getWebsite(search):
	url = 'http://en.wikipedia.org/wiki/' + search.replace(" ", "_")
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')
	site = urllib.request.urlopen(url)
	soup = BeautifulSoup(site)
	paras = soup.find_all('p')
	print('\n\n',paras[0].get_text())


def main():
	parser = argparse.ArgumentParser(prog="pywikidef",description="pywikidef") 
	parser.add_argument('--input', '-i', dest='search', help='Search a single term')
	parser.add_argument('--inputfile','-if',dest='inf', help='Input file with list of terms')
	args = parser.parse_args()
	search = args.search
	inf = args.inf
	if(search):
		getWebsite(search)
	if(inf):
		#terms = readInfile(inf)
		#print(terms)
		terms = ['John_Adams','George_Washington']
		for t in terms:
			getWebsite(t)
		

def readInfile(inp):
	inp.replace("\\","/")
	f = open(inp,'r')
	lines = f.readlines()
	for l in range(0,len(lines)):
		lines[l]=lines[l].replace(' ','_')
		lines[l]=lines[l].replace('\n','')
	f.close()
	return lines


if __name__ == '__main__':
	main()
