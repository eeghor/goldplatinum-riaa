from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

class GoldPlatinumArtistsRIAA:

	URL = 'https://www.riaa.com/gold-platinum/?tab_active=awards_by_artist#search_section'

	def __init__(self):

		# ChromeDriver is 2.38 available at https://chromedriver.storage.googleapis.com/2.38/chromedriver_mac64.zip
		self.DRIVER = webdriver.Chrome('webdriver/chromedriver')
		self.ARTISTS = set()

	def get(self):
		"""
		got to the right page on the RIAA web site and grab all artist names
		"""
		self.DRIVER.get(GoldPlatinumArtistsRIAA.URL)

		print('working...')

		THERES_MORE = True

		while THERES_MORE:

			WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='footer-content']")))

			try:
				self.DRIVER.find_element_by_id('loadmore').click()
				time.sleep(1)
			except:
				THERES_MORE = False

		for td in self.DRIVER.find_elements_by_class_name('artists_cell'):
			self.ARTISTS.add(td.text.lower().strip())

		self.DRIVER.close()

		print('done')

		return self

	def save(self, file):
		"""
		save collected artists into file in the collected directory
		"""

		if not os.path.exists('collected'):
			os.mkdir('collected')

		with open(f'collected/{file}','w') as f:
			for artist in sorted(artist for artist in self.ARTISTS):
				f.write(f'{artist}\n')

		print(f'saved {len(self.ARTISTS)} artists')


if __name__ == '__main__':

	gp = GoldPlatinumArtistsRIAA().get().save('goldplatinum-artists.txt')
