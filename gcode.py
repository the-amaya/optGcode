#!/usr/bin/env python3

import sys
import random, numpy, math, copy, matplotlib.pyplot as plt

t = ['Z2.5400']

with open(sys.argv[1]) as f:
	lines = [line.rstrip() for line in f]

def splitlist(sequence, sep):
	chunk = []
	for val in sequence:
		if any(i in val for i in sep):
			chunk.append(val)
			yield chunk
			chunk = []
		else:
			chunk.append(val)
	yield chunk

def cleancity(city):
	city = city[0]
	x = city.split()[2]
	y = city.split()[3]
	x = float(x[1:])
	y = float(y[1:])
	print(x,y)
	return x,y

listlist = []
for i in splitlist(lines,t):
	listlist.append(i)

listlist = list(filter(None, listlist))

count = len(listlist)
increment = 0
cities = []
while increment < count:
	cities.append(listlist[increment])
	increment += 1

plt.plot([cleancity(cities[i % count])[0] for i in range(count + 1)], [cleancity(cities[i % count])[1] for i in range(count + 1)], 'xb-');
plt.show()

tour = random.sample(range(count),count);
for temperature in numpy.logspace(0,5,num=10000000)[::-1]:
	[i,j] = sorted(random.sample(range(count),2));
	newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:];
	oldDistances = sum([ math.sqrt(sum([(cleancity(cities[tour[(k+1) % count]])[d] - cleancity(cities[tour[k % count]])[d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])
	newDistances = sum([ math.sqrt(sum([(cleancity(cities[newTour[(k+1) % count]])[d] - cleancity(cities[newTour[k % count]])[d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])
	if math.exp( ( oldDistances - newDistances) / temperature) > random.random():
		tour = copy.copy(newTour);
plt.plot([cleancity(cities[tour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[tour[i % count]])[1] for i in range(count + 1)], 'xb-');
plt.show()