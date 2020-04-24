###############
#selenium parser to get menu items for all restaurants in the US by city and food category
#done as the webscraping project during the NYCDSA bootcamp

from selenium import webdriver
import time
import collections

driver = webdriver.Chrome()

start_url  = "https://www.ubereats.com/location"

try:
	driver.get(start_url)
except:
	print("link broken\n")
	driver.close()
else: ##since successful opening start url proceed to unleash the spider
	location_links = {} #dict to store urls to all cities: location_links[city] = url
	location_category_links = collections.defaultdict(dict) #dict to store urls to categories within a city
															#location_category_links[city][category]= url
	restaurant_links_percity_percategory= collections.defaultdict(dict) #dict to store restaurant pages by [city][category]

	try:
		loc = driver.find_elements_by_xpath("//main//div//a")
	except:
		print("no links. something wrong\n")
		driver.close()
	else:
		city_cnt =0
		sep = "https://www.ubereats.com/location/"
		for link in loc:  ##get urls by city
			link = link.get_attribute("href")
			split_link = link.split(sep)
			if (split_link) and (len(split_link) == 2):
				city_cnt+=1
				print(f'processing link for city={split_link[1]}\tcity_count={city_cnt}')
				location_links[split_link[1]] = "https://www.ubereats.com/category/" + split_link[1]



	print("-"*50)
	####parse through list of locations urls to get links for each food category per city
	###put this in a for loop once you are ready
    ##list of cities = location_links.keys()
	city = "livingston-new-jersey"
	city_category_url = location_links[city] #replace with a loop variable

	for _ in range(1):  ###to be replaced by location_links.keys()
		try:
			driver.get(city_category_url)
			time.sleep(5)
		except:
			print(f'{city_category_url} is broken')
			time.sleep(5)
			continue

	###get all the category links on the city page
		try:
			cat = driver.find_elements_by_xpath("//main//div/h3/a")
		except:
			print(f'no category links for {city_category_url}')
			time.sleep(5)
			continue
		
		#cnt categories and form the links to each category per city in a dictionary of dictionaries
		cat_cnt =0
		stem_sep = "https://www.ubereats.com/category/"

		for cat_link in cat:
			cat_link = cat_link.get_attribute("href")
			sep = stem_sep + city +"/"
			split_link = cat_link.split(sep)
			if (split_link) and (len(split_link) == 2):
				cat_cnt+=1
				print(f'processing category={split_link[1]} for city={city} cat_count={cat_cnt} url:{cat_link}')
				location_category_links[city][split_link[1]] = cat_link



	###for each city and category get the links to restaurant pages with their menus.
		for category in location_category_links[city].keys():
			cat_link = location_category_links[city][category]

			try:
				driver.get(cat_link)
				time.sleep(5)
			except:
				print(f'{cat_link} is broken')
				time.sleep(5)
				continue

		###get all the links to restaurants in this category for this city!
			try:
				rest_links = driver.find_elements_by_xpath("//main//div/a")
			except:
				print(f'no restaurant links for {cat_link}')
				continue

			restaurant_list = []
			food_delivery = "/food-delivery/"
			for rl in rest_links:
				rl = rl.get_attribute("href")
				if food_delivery in rl:  ##strictly pick up only links relevant to the city being parsed
					restaurant_list.append(rl)

			restaurant_list = set(restaurant_list)
			restaurant_links_percity_percategory[city][category] = restaurant_list
			print(f'{category}')
			print("-"*50)
			print(restaurant_list)
			print("\n\n")

driver.close()