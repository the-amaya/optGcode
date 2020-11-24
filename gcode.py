#!/usr/bin/env python3

import sys
import random, numpy, math, copy, matplotlib.pyplot as plt

t = ['Z2.5400']
loop = 100
show = 0
tmp = 10000000
printEnd = "\r"

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
	#print(city)
	city = city[0]
	#x = city.split()[2]
	#y = city.split()[3]
	x = float(city.split()[2][1:])
	y = float(city.split()[3][1:])
	#print(x,y)
	return x,y

def fitness(localtour, citylist):
	#print(citylist)
	return sum([ math.sqrt(sum([(cleancity(cities[localtour[(k+1) % count]])[d] - cleancity(cities[localtour[k % count]])[d])**2 for d in [0,1] ])) for k in citylist])

def saucy(localtour):
	mlocaltour = list(localtour)
	print('saucy')
	for temperature in numpy.logspace(0,5,num=int(tmp/100))[::-1]:
		health = []
		for q in range(count):
			f = (fitness(mlocaltour, [q,(q - 1)]))
			health.append([f, q])
		health = sorted(health, key=lambda x: x[0], reverse=True)
		#print(len(health))
		#print(len([*range(count)[::-1]]))
		p = random.choices(health, weights = [*range(count)[::-1]])
		#print(p)
		i = int(p[0][1])
		#ihealth = fitness( )
		#print(i,j)
		plocaltour = list(mlocaltour)
		for j in range(count):
			#print('saucy j %d & i %d' % (j, i))
			newlocaltour = list(mlocaltour)
			newlocaltour[i], newlocaltour[j] = newlocaltour[j], newlocaltour[i]
			#print(plocaltour, newlocaltour)
			oldDistances = fitness(plocaltour, [j,j-1,i,i-1])
			newDistances = fitness(newlocaltour, [j,j-1,i,i-1])
			#print('oldDistances = %d - newDistances = %d' % (oldDistances, newDistances))
			if newDistances < oldDistances:
				#print('new plocal')
				plocaltour = list(newlocaltour)
				if show == 1:
					nd = fitness(mlocaltour, range(count))
					plt.clf()
					plt.suptitle('current fitness: %d  temp:%d run: %d -saucy time-' % (nd, temperature, rnd), ha='right')
					plt.plot([cleancity(cities[plocaltour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[plocaltour[i % count]])[1] for i in range(count + 1)], 'or-');
					plt.pause(0.01)
		mlocaltour = list(plocaltour)
		#print(f'\rsaucy temperature = {temperature}  health = {fitness(mlocaltour, range(count))}', end = printEnd)
	#print(mlocaltour)
	return mlocaltour

def randShuffle(tour):
	#print('run %d of %d' % (rnd, loop))
	#random.shuffle(tour)
	for temperature in numpy.logspace(0,5,num=tmp)[::-1]:
		[i,j] = sorted(random.sample(range(count),2));
		newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:];
		oldDistances = fitness(tour, [j,j-1,i,i-1])
		newDistances = fitness(newTour, [j,j-1,i,i-1])
		#pit = random.random()
		#dub = (oldDistances - newDistances) / temperature
		#moth = math.exp(dub)
		#print(oldDistances, newDistances, dub, moth, pit)
		#if moth > pit:
		if newDistances < (oldDistances + (temperature/10000)):
			tour = list(newTour);
			if show == 1:
				nd = fitness(newTour, range(count))
				plt.clf()
				plt.suptitle('current fitness: %d  temp:%d run: %d' % (nd, temperature, rnd), ha='right')
				plt.plot([cleancity(cities[tour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[tour[i % count]])[1] for i in range(count + 1)], 'or-');
				plt.pause(0.01)
	#kk.append(tour)
	newpath = fitness(tour, range(count))
	print('randShuffle fitness of run %d (lower is better): %d' % (rnd, newpath))
	return tour

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

tour = [*range(count)]
rnd = 0
mtour = tour
printEnd = "\r"

startDistance = fitness(range(count), range(count))
print('starting fitness: %d' % (startDistance))

plt.xkcd()
plt.suptitle('starting fitness: %d' % (startDistance), ha='right')
plt.plot([cleancity(cities[i % count])[0] for i in range(count + 1)], [cleancity(cities[i % count])[1] for i in range(count + 1)], 'or-');
#plt.show()
plt.pause(5.0)

while rnd < loop:
	rnd += 1
	ctour = saucy(randShuffle(tour))
	oldpath = fitness(mtour, range(count))
	newpath = fitness(ctour, range(count))
	print('fitness of run %d (lower is better): %d' % (rnd, newpath))
	if newpath < oldpath:
		mtour = list(ctour)
		plt.clf()
		plt.suptitle('overall best (shown): %d current run: %d' % (newpath, rnd), ha='right')
		plt.plot([cleancity(cities[mtour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[mtour[i % count]])[1] for i in range(count + 1)], 'or-');
		plt.pause(0.05)

#for i in range(loop):
finalDistances = fitness(mtour, range(count))
print('final fitness: %d' % (finalDistances))

plt.clf()
plt.suptitle('final fitness: %d' % (finalDistances), ha='right')
plt.plot([cleancity(cities[mtour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[mtour[i % count]])[1] for i in range(count + 1)], 'or-');
print('done')
plt.show()