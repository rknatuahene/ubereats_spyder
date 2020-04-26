# ubereats_spyder
uberEats(US) webscraper using selenium to pull in menus for data analysis
output of scraper is appended to file: 
	restaurant_menu_details.csv
scraper writes and reads from:
	visited_urls.csv  #all restaurant pages visited during last crawl
	finished_cities.csv #all cities whose restaurant pages have already been scraped via earlier crawls

uberEatsDA.ipynb - contains python scripts for pre-processing of data and some exploratory data analysis on the cleaned data.