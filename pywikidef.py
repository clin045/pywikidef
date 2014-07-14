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
	parser = argparse.ArgumentParser(prog="pywikidef", description="pywikidef")
	parser.add_argument('--input', '-i', dest='inp', required=True, help='What you are looking for')
	parser.add_argument('--amount', '-a', dest='amount', default=1, help='Amount of paragraphs')
	args = parser.parse_args()
	search = args.inp
	amount = int(args.amount)
	getWebsite(search, amount)

if __name__ == '__main__':
	main()