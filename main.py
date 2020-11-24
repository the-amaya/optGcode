#!/usr/bin/env python3

import math
import os

import matplotlib.pyplot as plt
import numpy
import random
import sys

t = ['Z2.5400']
loop = 100
show = 0
tmp = 10000000
printEnd = "\r"

#board size
boardx, boardy = 90, 70

#with open(sys.argv[1]) as f:
#	infilelines = [line.rstrip() for line in f]

with open('untitled.bot.etch.tap') as f:
	infilelines = [line.rstrip() for line in f]


def splitlist(sequence, sep):
	chunk = []
	for val in sequence:
		if any(ii in val for ii in sep):
			chunk.append(val)
			yield chunk
			chunk = []
		else:
			chunk.append(val)
	yield chunk


def cleancity(city):
	# print(city)
	city = city[0]
	# x = city.split()[2]
	# y = city.split()[3]
	x = float(city.split()[2][1:])
	y = float(city.split()[3][1:])
	# print(x,y)
	return x, y


def fitness(localtour, citylist, cities, count):
	# print(citylist)
	return sum([math.sqrt(sum(
		[(cleancity(cities[localtour[(k + 1) % count]])[d] - cleancity(cities[localtour[k % count]])[d]) ** 2 for d in [0, 1]])) for k in citylist])


def saucy(localtour, cities, count, rnd):
	mlocaltour = list(localtour)
	print('saucy')
	for temperature in numpy.logspace(0, 5, num=int(tmp / 100))[::-1]:
		health = []
		for q in range(count):
			f = (fitness(mlocaltour, [q, (q - 1)], cities, count))
			health.append([f, q])
		health = sorted(health, key=lambda x: x[0], reverse=True)
		# print(len(health))
		# print(len([*range(count)[::-1]]))
		p = random.choices(health, weights=[*range(count)[::-1]])
		# print(p)
		i = int(p[0][1])
		# ihealth = fitness( )
		# print(i,j)
		plocaltour = list(mlocaltour)
		for j in range(count):
			# print('saucy j %d & i %d' % (j, i))
			newlocaltour = list(mlocaltour)
			newlocaltour[i], newlocaltour[j] = newlocaltour[j], newlocaltour[i]
			# print(plocaltour, newlocaltour)
			oldDistances = fitness(plocaltour, [j, j - 1, i, i - 1], cities, count)
			newDistances = fitness(newlocaltour, [j, j - 1, i, i - 1], cities, count)
			# print('oldDistances = %d - newDistances = %d' % (oldDistances, newDistances))
			if newDistances < oldDistances:
				# print('new plocal')
				plocaltour = list(newlocaltour)
				if show == 1:
					nd = fitness(mlocaltour, range(count), cities, count)
					plt.clf()
					plt.suptitle('current fitness: %d  temp:%d run: %d -saucy time-' % (nd, temperature, rnd), ha='right')
					plt.plot([cleancity(cities[plocaltour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[plocaltour[i % count]])[1] for i in range(count + 1)], 'or-')
		plt.pause(0.01)
		mlocaltour = list(plocaltour)
	# print(f'\rsaucy temperature = {temperature}  health = {fitness(mlocaltour, range(count))}', end = printEnd)
	# print(mlocaltour)
	return mlocaltour


def randShuffle(tour, cities, count, rnd):
	# print('run %d of %d' % (rnd, loop))
	# random.shuffle(tour)
	for temperature in numpy.logspace(0, 5, num=tmp)[::-1]:
		[i, j] = sorted(random.sample(range(count), 2))
		newTour = tour[:i] + tour[j:j + 1] + tour[i + 1:j] + tour[i:i + 1] + tour[j + 1:]
		oldDistances = fitness(tour, [j, j - 1, i, i - 1], cities, count)
		newDistances = fitness(newTour, [j, j - 1, i, i - 1], cities, count)
		# pit = random.random()
		# dub = (oldDistances - newDistances) / temperature
		# moth = math.exp(dub)
		# print(oldDistances, newDistances, dub, moth, pit)
		# if moth > pit:
		if newDistances < (oldDistances + (temperature / 10000)):
			tour = list(newTour)
			if show == 1:
				nd = fitness(newTour, range(count), cities, count)
				plt.clf()
				plt.suptitle('current fitness: %d  temp:%d run: %d' % (nd, temperature, rnd), ha='right')
				plt.plot([cleancity(cities[tour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[tour[i % count]])[1] for i in range(count + 1)], 'or-')
				plt.pause(0.01)
	# kk.append(tour)
	newpath = fitness(tour, range(count), cities, count)
	print('randShuffle fitness of run %d (lower is better): %d' % (rnd, newpath))
	return tour


def originalopt():
	listlist = []
	for ii in splitlist(infilelines, t):
		listlist.append(ii)

	listlist = list(filter(None, listlist))

	count = len(listlist)
	increment = 0
	cities = []
	while increment < count:
		cities.append(listlist[increment])
		increment += 1

	tour = [*range(count)]
	rnd = 0
	mtour = tour

	startDistance = fitness(range(count), range(count), cities, count)
	print('starting fitness: %d' % startDistance)

	plt.xkcd()
	plt.suptitle('starting fitness: %d' % startDistance, ha='right')
	plt.plot([cleancity(cities[i % count])[0] for i in range(count + 1)], [cleancity(cities[i % count])[1] for i in range(count + 1)], 'or-')
	# plt.show()
	plt.pause(5.0)

	while rnd < loop:
		rnd += 1
		ctour = saucy(randShuffle(tour, cities, count, rnd), cities, count, rnd)
		oldpath = fitness(mtour, range(count), cities, count)
		newpath = fitness(ctour, range(count), cities, count)
		print('fitness of run %d (lower is better): %d' % (rnd, newpath))
		if newpath < oldpath:
			mtour = list(ctour)
			plt.clf()
			plt.suptitle('overall best (shown): %d current run: %d' % (newpath, rnd), ha='right')
			plt.plot([cleancity(cities[mtour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[mtour[i % count]])[1] for i in range(count + 1)], 'or-')
			plt.pause(0.05)

	# for i in range(loop):
	finalDistances = fitness(mtour, range(count), cities, count)
	print('final fitness: %d' % finalDistances)

	plt.clf()
	plt.suptitle('final fitness: %d' % finalDistances, ha='right')
	plt.plot([cleancity(cities[mtour[i % count]])[0] for i in range(count + 1)], [cleancity(cities[mtour[i % count]])[1] for i in range(count + 1)], 'or-')
	print('done')
	plt.show()


def cleangcode(l):
	oo = []
	for l in l:
		if any(i in l.split()[1] for i in ['G00', 'G01']):
			if float(l.split()[2][1:]) == 0 and float(l.split()[3][1:]) == 0:
				pass
			else:
				oo.append(l)
	return oo


def minsize(l):
	minx, maxx, miny, maxy = boardx, 0.0, boardy, 0.0
	for line in l:
		if len(line.split()) >= 4:
			if line.split()[2][:1] == 'X' and line.split()[3][:1] == 'Y':
				if float(line.split()[2][1:]) == 0 and float(line.split()[3][1:]) == 0:
					pass
				else:
					if float(line.split()[2][1:]) < float(minx):
						minx = float(line.split()[2][1:])
					if float(line.split()[2][1:]) > float(maxx):
						maxx = float(line.split()[2][1:])
					if float(line.split()[3][1:]) < float(miny):
						miny = float(line.split()[3][1:])
					if float(line.split()[3][1:]) > float(maxy):
						maxy = float(line.split()[3][1:])
	totalx = maxx - minx
	totaly = maxy - miny
	return minx, miny, totalx, totaly


def transposegcode(l, mx, my):
	oo = []
	for line in l:
		if len(line.split()) >= 4:
			if line.split()[2][:1] == 'X' and line.split()[3][:1] == 'Y':
				if float(line.split()[2][1:]) == 0 and float(line.split()[3][1:]) == 0:
					pass
				else:
					linelist = line.split()
					linelist[2] = ('X' + str(round((float(linelist[2][1:]) + mx), 4)))
					linelist[3] = ('Y' + str(round((float(linelist[3][1:]) + my), 4)))
					line = ' '.join(linelist)
		oo.append(line)
	return oo


def dumpoutput(l):
	w = open('output.txt', 'w')
	for l in l:
		w.write(l + "\n")


def nestcalc(totx, toty):
	nestx = math.floor(boardx / totx)
	nesty = math.floor(boardy / toty)
	offx = boardx / nestx
	offy = boardy / nesty
	return nestx, nesty, offx, offy


def nestmake(l, nestxcount, nestycount, offxmm, offymm, totx, toty):
	oo = []
	padx = (offxmm - totx) / 2
	pady = (offymm - toty) / 2
	for nsty in range(nestycount):
		for nstx in range(nestxcount):
			ttx = (nstx * offxmm) + padx
			tty = (nsty * offymm) + pady
			s = (transposegcode(l, ttx, tty))
			for d in s:
				oo.append(d)
	return oo


def ploter(x, y, pram):
	#plt.xkcd()
	plt.plot(x, y, **pram)


def plothelp(l):
	for ii in splitlist(l, t):
		xx = []
		yy = []
		for line in ii:
			if len(line.split()) >= 4:
				if line.split()[2][:1] == 'X' and line.split()[3][:1] == 'Y':
					if float(line.split()[2][1:]) == 0 and float(line.split()[3][1:]) == 0:
						pass
					else:
						linelist = line.split()
						xx.append(float(linelist[2][1:]))
						yy.append(float(linelist[3][1:]))
		ploter(xx, yy, {'marker': ''})
	plt.show()



while True:
	# os.system('clear')
	print('Please use the following commands (do not include parenthesies in your commands)')
	print('min-size -this function will determine the minimum xy size of a gcode file')
	print('nest -this function will attempt to nest gcode -currently uses a hard coded board size')

	usrip = input()

	if usrip == 'min-size':
		dumpoutput(transposegcode(infilelines, -minsize(infilelines)[0], -minsize(infilelines)[1]))

	elif usrip == 'nest':
		cleancode = cleangcode(infilelines)
		plothelp(cleancode)
		minx, miny, totx, toty = minsize(cleancode)
		nestx, nesty, offx, offy = nestcalc(totx, toty)
		minimizedcode = transposegcode(cleancode, -minx, -miny)
		plothelp(minimizedcode)
		nestedgcode = nestmake(minimizedcode, nestx, nesty, offx, offy, totx, toty)
		plothelp(nestedgcode)
		dumpoutput(nestedgcode)

	else:
		print("You have two options, why dont you try again and see if you can figure this out")
		input()