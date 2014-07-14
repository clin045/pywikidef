from bs4 import BeautifulSoup
import urllib.request
import argparse

def getWebsite(search, amount):
	url = 'http://en.wikipedia.org/wiki/' + search.replace(" ", "_")
	site = urllib.request.urlopen(url)
	soup = BeautifulSoup(site)
	soup.prettify()
	paras = soup.find_all('p')
	for index in range(amount):
		try:
			output = str(paras[index].get_text()).encode(errors='backslashreplace')
			print(output)
		except IndexError:
			print("\n\nThere are no more paragraphs")
			break
def main():
	parser = argparse.ArgumentParser(prog="pywikidef",description="pywikidef") 
	parser.add_argument('--input', '-i', dest='search', help='Search a single term')
	parser.add_argument('--inputfile','-if',dest='inf', help='Input file with list of terms')
	parser.add_argument('--amount', '-a', dest='amount', default=1, help='Amount of paragraphs')
	args = parser.parse_args()
	search = args.search
	amount = int(args.amount)
	inf = args.inf
	if(search):
		getWebsite(search)
	if(inf):
		terms = readInfile(inf)
		for t in terms:
			print('\n\n')
			getWebsite(t, amount)
		

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
