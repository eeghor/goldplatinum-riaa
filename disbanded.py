from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import sys
import os

class Disb:

	def __init__(self):

		self.WIKICAT_URL = 'https://en.wikipedia.org/wiki/Category:Musical_groups_disestablished_in_'
		self.DATADIR = 'data'
		self.YEARS = [y for y in range(1950, 2019)]

		self.URLS = [f'{self.WIKICAT_URL}{_}' for _ in self.YEARS]

		self.perfs_names = set()

	def get(self):

		for url in self.URLS:

			print(url)

			soup = BeautifulSoup(requests.get(url).text, 'lxml')	
			
			possible_class_names = ['mw-category-group', 'mw-content-ltr']

			for pc in possible_class_names:

				_found_divs = soup.find_all('div', class_=pc)

				if not _found_divs:
					continue
				else:
					for _ in _found_divs:
						for li_ in _.find_all('li'):
							self.perfs_names.add(unidecode(li_.text.lower().split('(')[0].strip()))
					break

		return self

	def save(self):

		fname = f'res.txt'

		if not os.path.exists(self.DATADIR):
			os.mkdir(self.DATADIR)

		if self.perfs_names:
			with open(os.path.join(self.DATADIR, fname), 'w') as f:
				for _ in self.perfs_names:
					f.write(f'{_}\n')

		print(f'saved {len(self.perfs_names)} to file {fname}')

		return self


if __name__ == '__main__':

	sp = Disb().get().save()
