import csv
import requests
import pandas as pd
from io import StringIO
from os import listdir

# url = "https://www.mountainproject.com/route-finder-export?"\
# 	"diffMaxaid=75260&diffMaxboulder=20050&diffMaxice=38500&diffMaxmixed=60000&diffMaxrock="+"2500"+"&"\
# 	"diffMinaid=70000&diffMinboulder=20000&diffMinice=30000&diffMinmixed=50000&diffMinrock="+"2300"+"&"\
# 	"is_sport_climb=1&is_top_rope=1&is_trad_climb=1&pitches=0&selectedIds=105720495&"\
# 	"sort1=popularity+desc&sort2=rating&stars=0&type=rock&viewAll=1"

# response = requests.get(url).text
# df = pd.read_csv(StringIO(response))


# Some functions to help with processing dataframe

def get_id(route_url):
	""" extracts numbers from url"""
	return ''.join([dig for dig in route_url if str.isdigit(dig)])

def convert_grade(rating):
	"""take X out of 5.XX"""
	if rating[0] != '5':
		return None
	elif all(map(str.isdigit, rating[2:4])):
		return rating[2:4]
	elif str.isdigit(rating[2]):
		return rating[2]
	else:
		return None

def check_safety(rating):
	"""check if R/X/PG13"""
	if 'R' in rating:
		return 'R'
	elif 'PG13' in rating:
		return 'PG13'
	elif 'X' in rating:
		return 'X'
	else:
		return 'S'

def get_routes_by_diff(min_grade, max_grade):
	"""
	Downloads all climbs in grade range as a single csv
	Takes in numbers rather than strings
	"""
	min_g = str(min_grade)
	max_g = str(max_grade)
	url = "https://www.mountainproject.com/route-finder-export?"\
	"diffMaxaid=75260&diffMaxboulder=20050&diffMaxice=38500&diffMaxmixed=60000&diffMaxrock="+max_g+"&"\
	"diffMinaid=70000&diffMinboulder=20000&diffMinice=30000&diffMinmixed=50000&diffMinrock="+min_g+"&"\
	"is_sport_climb=1&is_top_rope=1&is_trad_climb=1&pitches=0&selectedIds=105720495&"\
	"sort1=popularity+desc&sort2=rating&stars=0&type=rock&viewAll=1"

	response = requests.get(url).text
	df = pd.read_csv(StringIO(response), dtype = str)

	# Executing the processing
	df['id'] = df.URL.apply(get_id)
	df['location'] = df.Location.apply(lambda string : str.split(string, ' > ') )
	df['grade'] = df.Rating.apply(convert_grade)
	df['safety'] = df.Rating.apply(check_safety)
	df = df.drop(columns = ['Location', 'Your Stars'])

	df.to_csv('data/jt'+min_g+'_'+max_g+'.csv', index = False)

def get_all_routes():
	"""
	Downloads all the routes for Josha tree, saved in seperate csv files
	"""
	# get 5.0 to 5.5
	for i in range(1000, 1600, 100):
		get_routes_by_diff(i ,i)
	# get 5.6 and 5.7
	get_routes_by_diff(1600 ,1700)
	get_routes_by_diff(1800 ,1900)
	# get 5.8 and harder 
	for i in range(2000,12400,300):
		get_routes_by_diff(i, i+200)

def merge_files():
	df = pd.concat([pd.read_csv(('data/'+filename), dtype = str) for filename in listdir('data')])
	df = df.rename(columns = {'Rating': 'rating', 'Route Type': 'type', 'Avg Stars':'stars',
		'Pitchees':'pitches', 'Area Latitude': 'latitude', 'Area Longitude':'longitude', 
		'Pitches':'pitches'})
	df.to_csv('app_data/whole_jt_data.csv', index = False)


