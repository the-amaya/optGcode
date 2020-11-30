#!/usr/bin/env python3

import math
import os

import matplotlib.pyplot as plt
import numpy
import random
import sys

t = ['Z2.5400']
loop = 1
show = 0
tmp = 10000
printEnd = "\r"

#board size
boardx, boardy = 90, 70
zdown, zup = '0.2500', '2.5400'

#with open(sys.argv[1]) as f:
#	infilelines = [line.rstrip() for line in f]

with open('demo/untitled.bot.etch.tap') as f:
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
	#print(city)
	city = city[0]
	#print(city)
	# x = city.split()[2]
	# y = city.split()[3]
	x = float(city.split()[2][1:])
	y = float(city.split()[3][1:])
	# print(x,y)
	return x, y


def fitness(localtour, citylist, cities, count):
	#TODO refactor this function
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


def originalopt(l):
	listlist = []
	for ii in splitlist(l, t):
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
	plt.pause(2.0)

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
	sort = []
	oo = []
	for i in range(count + 1):
		sort.append(cities[mtour[i % count]])
	#print(sort)
	for i in range(count ):
		for p in range(len(sort[i])):
			oo.append(sort[i][p])
	return oo


def cleangcode(l):
	oo = []
	for l in l:
		if any(i in l.split()[1] for i in ['G00', 'G01']):
			if float(l.split()[2][1:]) == 0 and float(l.split()[3][1:]) == 0:
				pass
			else:
				oo.append(l)
	if oo[0].split()[2] == 'Z2.5400':
		oo.pop(0)
	if oo[-1].split()[2] == 'Z3.5000':
		oo.pop(-1)
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


def dumpoutput(l, n):
	l.insert(0, f'N0 G21')
	l.insert(1, f'N0 G90')
	l.insert(2, f'N0 G00 Z{zup}')
	l.insert(3, f'N0 G00 X0.0000 Y0.0000')
	l = fixlinenumbers(l)
	n = str(n) + '.txt'
	w = open(n, 'w')
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
					if 1==2:#float(line.split()[2][1:]) == 0 and float(line.split()[3][1:]) == 0:
						#todo this check is probably not needed here and it breaks plotting of the boarder
						pass
					else:
						linelist = line.split()
						xx.append(float(linelist[2][1:]))
						yy.append(float(linelist[3][1:]))
		ploter(xx, yy, {'marker': ''})
	plt.show()


def fixlinenumbers(l):
	oo = []
	pad = len(str(len(l) * 10))
	for i in range(len(l)):
		num = i * 10
		num = str(num).zfill(pad)
		linelist = l[i].split()
		linelist[0] = ('N' + str(num))
		line = ' '.join(linelist)
		oo.append(line)
	return oo


def scorelines(xc, yc, xo, yo, xm, ym, etchdepth, zup, border):
	nx = 0
	ny = 0
	oo = []
	oo.append(f'N0 G00 Z{zup}')
	for i in range(xc - 1):
		nx = nx + xo
		oo.append(f'N0 G00 X{nx} Y0.0')
		oo.append(f'N0 G01 Z-{etchdepth} F200.00')
		oo.append(f'N0 G01 X{nx} Y{ym} F200.00')
		oo.append(f'N0 G00 Z{zup}')
	for i in range(yc - 1):
		ny = ny + yo
		oo.append(f'N0 G00 X0.0 Y{ny}')
		oo.append(f'N0 G01 Z-{etchdepth} F200.00')
		oo.append(f'N0 G01 X{xm} Y{ny} F200.00')
		oo.append(f'N0 G00 Z{zup}')
	if border == 1:
		oo.append(f'N0 G00 X0.0 Y0.0')
		oo.append(f'N0 G01 Z-{etchdepth} F200.00')
		oo.append(f'N0 G01 X0.0 Y{ym} F200.00')
		oo.append(f'N0 G01 X{xm} Y{ym}')
		oo.append(f'N0 G01 X{xm} Y0.0')
		oo.append(f'N0 G01 X0.0 Y0.0')
		oo.append(f'N0 G00 Z{zup}')
	return oo


def nesthandler(score, borders):
	cleancode = cleangcode(infilelines)
	plothelp(cleancode)
	minx, miny, totx, toty = minsize(cleancode)
	nestx, nesty, offx, offy = nestcalc(totx, toty)
	minimizedcode = transposegcode(cleancode, -minx, -miny)
	plothelp(minimizedcode)
	nestedgcode = nestmake(minimizedcode, nestx, nesty, offx, offy, totx, toty)
	if score == 1:
		scoresheet = scorelines(nestx, nesty, offx, offy, boardx, boardy, zdown, zup, borders)
		for i in scoresheet:
			nestedgcode.append(i)
	plothelp(nestedgcode)
	dumpoutput(nestedgcode, 'output')

#TODO handle file headers and footers

while True:
	# os.system('clear')
	print('Please use the following commands (do not include parenthesies in your commands)')
	print('min-size -this function will determine the minimum xy size of a gcode file')
	print('nest -this function will attempt to nest gcode -currently uses a hard coded board size')
	print('the \'test\' function is undocumented. currently it runs a short optimization routine')

	usrip = input()

	if usrip == 'min-size':
		dumpoutput(transposegcode(infilelines, -minsize(infilelines)[0], -minsize(infilelines)[1]), 'min')

	elif usrip == 'nest':
		nesthandler(1, 1)
	
	elif usrip == 'test':
		dumpoutput(fixlinenumbers(originalopt(cleangcode(infilelines))), 'test')

	else:
		print("You have two options, why dont you try again and see if you can figure this out")
		input()