import csv
import requests
import pandas as pd
from io import StringIO

url = "https://www.mountainproject.com/route-finder-export?"\
	"diffMaxaid=75260&diffMaxboulder=20050&diffMaxice=38500&diffMaxmixed=60000&diffMaxrock="+"2500"+"&"\
	"diffMinaid=70000&diffMinboulder=20000&diffMinice=30000&diffMinmixed=50000&diffMinrock="+"2300"+"&"\
	"is_sport_climb=1&is_top_rope=1&is_trad_climb=1&pitches=0&selectedIds=105720495&"\
	"sort1=popularity+desc&sort2=rating&stars=0&type=rock&viewAll=1"

response = requests.get(url).text
df = pd.read_csv(StringIO(response))


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

# Executing the processing

df['id'] = df.URL.apply(get_id)
df['location'] = df.Location.apply(lambda string : str.split(string, ' > ') )
df['grade'] = df.URL.apply(convert_grade)
df['safety'] = df.URL.apply(check_safety)
df = df.drop(columns = ['Location', 'Your Stars'])

df.to_csv("test", index = False)




