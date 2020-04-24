###############
#selenium parser to get menu items for all restaurants in the US by city and food category
#done as the webscraping project during the NYCDSA bootcamp

from selenium import webdriver
import time
import collections
import re

driver = webdriver.Chrome()

start_url  = "https://www.ubereats.com/location"

try:
	driver.get(start_url)
except:
	print("link broken\n")
	driver.close()
else: 
	##since successful opening start url proceed to unleash the spider
	location_links = {} #dict to store urls to all cities: location_links[city] = url
	location_category_links = collections.defaultdict(dict) #dict to store urls to categories within a city
															#location_category_links[city][category]= url
	restaurant_links_percity_percategory= collections.defaultdict(dict) #dict to store restaurant pages by [city][category]
	restaurant_master_dict = collections.defaultdict(dict)

	fp = open('restaurant_info.csv', 'w')
	fp.write(f'uber_city,name,food_category,priciness_level,ratings,num_reviews,street_address,local_city,state,zipcode' +'\n')

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


		cnt =0 
	###for each city and category get the links to restaurant pages with their menus.
		for category in location_category_links[city].keys():
			## do this for only 5 categories for now
			if cnt > 1:
				break
			else:
				cnt+=1
			## do this for only 5 categories for now

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


	####Now get restaurant details for each page:
	# attributes: restaurant_name, rest_food_category, rest_priciness, street_address, city, state, zipcode
		def cleanRestaurantString(s):
			if s:
				s = s.strip()
				return s.split("\n")[0]
			return ""

		cntr = 0
		while cntr < 1:
			cntr+=1
			for city in restaurant_links_percity_percategory.keys():
				for category in restaurant_links_percity_percategory[city].keys():
					for restaurant_page in restaurant_links_percity_percategory[city][category]:
						restaurant_name = ""
						rest_food_category = ""
						rest_priciness = ""
						street_address = ""
						local_city = ""
						(state, zipcode) = ("","")

						try:
							driver.get(restaurant_page)
							time.sleep(5)
						except:
							print("link broken\n")
							continue

						try:
							restaurant_name = driver.find_element_by_xpath('//div//h1').text

						except:
							print(f'{restaurant_page} is not valid')
							continue
						else:
							pricey_restaurant_type = driver.find_element_by_xpath('//div//h1//following-sibling::div').text
							s = list(map(str.strip, pricey_restaurant_type.split('•')))
							if len(s) >=2:
								rest_food_category = ','.join(s[1:])
								rest_priciness = s[0] 
							

							###get restaurant address
							restaurant_address = driver.find_element_by_xpath('//div//p').text
							addy = restaurant_address.split(',')

							addy = list(map(cleanRestaurantString, addy))
							if len(addy) > 2:
								street_address = addy[0]
								local_city = addy[1]
								group = re.search('([a-zA-Z\s]+)(\d+)', addy[2])
								
								try:
									state = group[1].strip()
									zipcode = group[2].strip()
								except:
									print(f'could not get state and zipcode. moving on')
									continue
							
							try:
								ratings_info = driver.find_element_by_xpath('//div[contains(text(),"View delivery time")]//parent::div').text
							except:
								print("no ratings so moving on\n")
								continue

							ratings_info = ratings_info.split("\n")
							if len(ratings_info) > 1:
								ratings = ratings_info[0].strip()
								ratings = re.sub('[^0-9\.]','',ratings).strip(".")
								num_reviews = re.sub('[\(\)]','',ratings_info[1])
								num_reviews = re.sub('\D','',num_reviews)

							print(f'name:{restaurant_name}')
							print(f'food_category:{rest_food_category}')
							print(f'priciness_level:{rest_priciness}')
							print(f'ratings_why:{ratings}')
							print(f'num_reviews_why:{num_reviews}')
							print(f'street_addy:{street_address}')
							print(f'city:{local_city}')
							print(f'state:{state}')
							print(f'zipcode:{zipcode}')
							print("-"*50)
							restaurant_master_dict[restaurant_name]["name"] = restaurant_name
							restaurant_master_dict[restaurant_name]["food_category"] = rest_food_category
							restaurant_master_dict[restaurant_name]["priciness_level"] = rest_priciness
							restaurant_master_dict[restaurant_name]["rating"] = ratings
							restaurant_master_dict[restaurant_name]["num_reviews"] = num_reviews
							restaurant_master_dict[restaurant_name]["street_address"] = street_address
							restaurant_master_dict[restaurant_name]["address_city"] = local_city
							restaurant_master_dict[restaurant_name]["state"] = state
							restaurant_master_dict[restaurant_name]["zipcode"] = zipcode
			print(f'done processing city:{city}')
			print(f'writing data to file')
			for restaurant_name in restaurant_master_dict.keys():
				food_category	=		restaurant_master_dict[restaurant_name]["food_category"]
				priciness_level	=		restaurant_master_dict[restaurant_name]["priciness_level"]
				ratings			=		restaurant_master_dict[restaurant_name]["rating"]
				num_reviews		=		restaurant_master_dict[restaurant_name]["num_reviews"]
				street_address	=		restaurant_master_dict[restaurant_name]["street_address"]
				local_city		=		restaurant_master_dict[restaurant_name]["address_city"]
				state			=		restaurant_master_dict[restaurant_name]["state"] 
				zipcode			=		restaurant_master_dict[restaurant_name]["zipcode"]
				fp.write(f'{city},{restaurant_name},\"{food_category}\",{priciness_level},{ratings},{num_reviews},\"{street_address}\",{local_city},{state},{zipcode}' +'\n')
fp.close()
driver.close()