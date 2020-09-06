# more required packages -
# requests, json, need to check for this so that it runs


# TO DO:

# routes and routes confusing
# can make the class tidier

import MountainProjectPublicAPI as mp
import csv
import pandas as pd


# Read in the prviate key
f = open('credential.txt')
key = f.read()
f.close()


# Default for Joshua Tree
j_lat = 34.012
j_long = -116.168


def get_climbs():
	'''
	Downloads the climbs in a radius of the base coordinates
	'''
	json_routes = mp.getRoutesForLatLon(key, j_lat, j_long, maxDiff = '5.15d')
	return json_routes['routes']


# class to store route info
class route():
	def __init__(self, id, name, type, rating, stars, starVotes, pitches, location, longitude, latitude):
		self.id = id
		self.name = name
		self.type = type
		self.rating = rating
		self.stars = stars
		self.starVotes = starVotes
		self.pitches = pitches
		self.location = location
		self.longitude = longitude
		self.latitude = latitude
		self.check_safety()
		self.convert_grade()

	def convert_json(json):
		"""reads json to make a route""" 
		new_route = route(json['id'], json['name'], json['type'], json['rating'],
			json['stars'], json['starVotes'], json['pitches'], json['location'],
			json['longitude'], json['latitude'])
		#new_route.check_safety()
		#new_route.convert_grade()
		return new_route

	def convert_grade(self):
		"""take X out of 5.XX"""
		if self.rating[0] != '5':
			self.grade = None
		elif all(map(str.isdigit, self.rating[2:4])):
			self.grade = self.rating[2:4]
		elif str.isdigit(self.rating[2]):
			self.grade = self.rating[2]
		else:
			self.grade = None


	def check_safety(self):
		"""check if R/X/PG13"""
		if 'R' in self.rating:
			self.safety = 'R'
		elif 'PG13' in self.rating:
			self.safety = 'PG13'
		elif 'X' in self.rating:
			self.safety = 'X'
		else:
			self.safety = 'S'

	def route_to_dict(self):
		return self__dict__


def routes_to_csv(routes, file_name = 'names.csv'):
	first = route.convert_json(routes[0])
	fieldnames = vars(first).keys()
	f = open(file_name, 'w', newline= '')
	writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
	writer.writeheader()
	for r in routes:
		writer.writerow(vars(route.convert_json(r)))




# def routes_to_csv(routes, fieldnames):
# 	'''
# 	Writes a list of routes to csv, only taking the relevant columns 
# 	'''
# 	with open('names.csv', 'w', newline='') as csvfile:
# 	    #fieldnames = ['id', 'rating','stars','type', 'longitude','latitude']
# 	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
# 	    writer.writeheader()
# 	    for line in routes:
# 	    	writer.writerow(line)


