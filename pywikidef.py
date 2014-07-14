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
	soup.prettify()
	print(soup)


def main():
	parser = argparse.ArgumentParser(prog="pywikidef", 
							description="pywikidef")
	parser.add_argument('--input', '-i', dest='search', required=True,
							help='What you are looking for')
	args = parser.parse_args()
	search = args.search
	getWebsite(search)


if __name__ == '__main__':
	main()
