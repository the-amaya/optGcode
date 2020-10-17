#!/usr/bin/env python3

import sys
import random, numpy, math, copy, matplotlib.pyplot as plt

t = ['Z2.5400']
loop = 10
show = 1

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
	#x = city.split()[2]
	#y = city.split()[3]
	x = float(city.split()[2][1:])
	y = float(city.split()[3][1:])
	#print(x,y)
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

#plt.plot([cleancity(cities[i % count])[0] for i in range(count + 1)], [cleancity(cities[i % count])[1] for i in range(count + 1)], 'xb-');
#plt.pause(0.05)

tour = random.sample(range(count),count);
rnd = 0
mtour = tour
printEnd = "\r"

startDistance = sum([ math.sqrt(sum([(cleancity(cities[(k+1) % count])[d] - cleancity(cities[k % count])[d])**2 for d in [0,1] ])) for k in range(count)])
print('starting fitness: %d' % (startDistance))

plt.xkcd()
plt.suptitle('starting fitness: %d' % (startDistance), ha='right')
plt.plot([cleancity(cities[i % count])[0] for i in range(count + 1)], [cleancity(cities[i % count])[1] for i in range(count + 1)], 'or-');
plt.show()

while rnd < loop:
	rnd += 1
	#print('run %d of %d' % (rnd, loop))
	random.shuffle(tour)
	for temperature in numpy.logspace(0,5,num=100000)[::-1]:
		[i,j] = sorted(random.sample(range(count),2));
		newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:];
		oldDistances = sum([ math.sqrt(sum([(cleancity(cities[tour[(k+1) % count]])[d] - cleancity(cities[tour[k % count]])[d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])
		newDistances = sum([ math.sqrt(sum([(cleancity(cities[newTour[(k+1) % count]])[d] - cleancity(cities[newTour[k % count]])[d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])
		#pit = random.random()
		#dub = (oldDistances - newDistances) / temperature
		#moth = math.exp(dub)
		#print(oldDistances, newDistances, dub, moth, pit)
		#if moth > pit:
		if newDistances < (oldDistances + (temperature/1000)):
			tour = copy.copy(newTour);
			if show == 1:
				nd = sum([ math.sqrt(sum([(cleancity(cities[newTour[(k+1) % count]])[d] - cleancity(cities[newTour[k % count]])[d])**2 for d in [0,1] ])) for k in range(count)])
				plt.clf()
				plt.suptitle('current fitness: %d  temp:%d' % (nd, temperature), ha='right')
				plt.plot([cleancity(cities[tour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[tour[i % count]])[1] for i in range(count + 1)], 'or-');
				plt.pause(0.01)
	#kk.append(tour)
	oldpath = sum([ math.sqrt(sum([(cleancity(cities[mtour[(k+1) % count]])[d] - cleancity(cities[mtour[k % count]])[d])**2 for d in [0,1] ])) for k in range(count)])
	newpath = sum([ math.sqrt(sum([(cleancity(cities[tour[(k+1) % count]])[d] - cleancity(cities[tour[k % count]])[d])**2 for d in [0,1] ])) for k in range(count)])
	#print()
	print('fitness of run %d (lower is better): %d' % (rnd, newpath))
	if newpath < oldpath:
		mtour = copy.copy(tour)

#for i in range(loop):
finalDistances = sum([ math.sqrt(sum([(cleancity(cities[mtour[(k+1) % count]])[d] - cleancity(cities[mtour[k % count]])[d])**2 for d in [0,1] ])) for k in range(count)])
print('final fitness: %d' % (finalDistances))

plt.clf()
plt.suptitle('final fitness: %d' % (finalDistances), ha='right')
plt.plot([cleancity(cities[mtour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[mtour[i % count]])[1] for i in range(count + 1)], 'or-');
print('done')
plt.show()