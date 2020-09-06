# required packages - requests, json, need to check for this

import MountainProjectPublicAPI as mp
import csv
import pandas as pd


# Read in the prviate key 
f = open('credential.txt')
key = f.read()
f.close()


j_lat = 34.012
j_long = -116.168

def get_climbs():
	'''
	Downloads the climbs in a radius of the base coordinates
	'''
	json_routes = mp.getRoutesForLatLon(key, j_lat, j_long, maxDiff = '5.15d')
	return json_routes['routes']

def routes_to_csv(routes):
	'''
	Writes a list of routes to csv, only taking the relevant columns 
	'''
	with open('names.csv', 'w', newline='') as csvfile:
	    fieldnames = ['id', 'rating','stars','type', 'longitude','latitude']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
	    writer.writeheader()
	    for line in routes:
	    	writer.writerow(line)



