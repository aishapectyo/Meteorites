#!/usr/bin/env python
"""
Intro. to using NASA's API and Python's Pandas.
Meteorite Landings (1400-today)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.basemap import Basemap
import csv
import pandas as pd
import json 
import urllib
import unicodedata
from collections import Counter
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

#Acquire Nasa's data.
get_data = ("https://data.nasa.gov/resource/gh4g-9sfh.json")
#Put in json format
meteor_data = pd.read_json(get_data)

#Analyze/Visualize Data
#Check class and mass frequency in grams)
class_frequency = Counter(meteor_data['recclass']).most_common()
masses_frequency = Counter(meteor_data['mass']).most_common()
mass = [x[0] for x in masses_frequency]
mass_frequency =  [x[1] for x in masses_frequency]
types = [y[0] for y in class_frequency]
type_frequency = [y[1] for y in class_frequency]

#Change type to unicode
meteor_type = []
for n in xrange(len(types)):
	notuni =  unicodedata.normalize('NFKD', types[n]).encode('ascii','ignore')
	meteor_type.append(notuni)

#Divide data by size of meteorite
long = np.array(meteor_data['reclong'])
lat = np.array(meteor_data['reclat'])
all_mass = np.array(meteor_data['mass'])
all_mass_len = len(all_mass)
long_less_20 = []
lat_less_20 = []
long_bigger_20 = []
lat_bigger_20 = []
for j in xrange(all_mass_len):
	if all_mass[j] < 2000000:
		long_less_20.append(long[j])
		lat_less_20.append(lat[j])
	else:
		long_bigger_20.append(long[j])
		lat_bigger_20.append(lat[j])


#Make meteorite map
meteor_map = Basemap(projection='cyl', lat_0 = 0, lon_0 = -45.5, resolution='l', area_thresh=1000.0)
meteor_map.drawcoastlines()
meteor_map.fillcontinents(color='black', alpha = 0.7)
meteor_map.drawcountries()
meteor_map.drawmeridians(np.arange(0, 360,30))
meteor_map.drawparallels(np.arange(-90, 90, 30))
x_long_small, y_lat_small = meteor_map(long_less_20, lat_less_20)
x_long_big, y_lat_big = meteor_map(long_bigger_20, lat_bigger_20)
meteor_map.plot(x_long_small,y_lat_small,'ro', markersize=4.5, alpha = 0.58)
meteor_map.plot(x_long_big,y_lat_big,'go', markersize=8, alpha = 0.58)
plt.show()

#Make Other Plots
data = Data([Bar(x=['L6', 'H5', 'H6', 'L5', 'H4'],y=[241, 143, 79, 68, 48], marker=Marker(color='rgb(142, 124, 195)'))])
layout = Layout(title='Meteorite Type',font=Font(family='Raleway, sans-serif'),showlegend=False,xaxis=XAxis(tickangle=-45),yaxis=YAxis(zeroline=False,gridwidth=2),bargap=0.05)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='metmasses')

year_frequency = Counter(meteor_data['year']).most_common()
yr = [x[0] for x in year_frequency]
cn = [x[1] for x in year_frequency]
yrs_full = []
for n in xrange(len(yr)):
	notuni =  unicodedata.normalize('NFKD', yr[n]).encode('ascii','ignore')
	yrs_full.append(notuni)
yr_only = []
for n in xrange(len(yrs_full)):
	splitting = (yrs_full[n].split('-'))
	splitting = int(splitting[0])
	yr_only.append(splitting)

data = Data([Scatter(x= yr_only, y = cn)])
plot_url = py.plot(data, filename='date-axes')
