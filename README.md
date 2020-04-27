# ubereats_spyder
uberEats(US) webscraper using selenium to pull in menus for data analysis
output of scraper is appended to file: 
	restaurant_menu_details.csv
scraper writes and reads from:
	visited_urls.csv  #all restaurant pages visited during last crawl
	finished_cities.csv #all cities whose restaurant pages have already been scraped via earlier crawls

uberEatsDA.ipynb - contains python scripts for pre-processing of data and some exploratory data analysis on the cleaned data.

a cut of the output data representing scraped data for restaurants in Arizona and Alabama is being uploaded to github to support
the exploratory data analysis work found the python notebook. Filename for the cut is restaurant_menu_details_DA_copy.csv
this file has been cleaned up to account for read_csv not picking up strings with embedded quotation marks in them properly in spite
of having enclosed the entire string in quotes.