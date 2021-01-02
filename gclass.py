class Gline:

	def __init__(self, *, linetype, **kwargs):
		# TODO absolute line number counter
		self.type = linetype
		# self.aln = aln
		if 'fln' in kwargs:
			self.fln = kwargs.get('fln')
		if linetype == 'comment':
			# comment line
			# ideally these will only be at teh start of the file
			# but we will keep their relative position in the file as best we can
			self.comment = kwargs.get('comment')
		elif linetype == 'G':
			# G lines should include a 'g' kwarg equal to the supported gcode command.
			if kwargs.get('g') == 'G21':
				# metric mode
				# this may do something in the program in the future if I support other modes of operations
				self.g = 'G21'
			if kwargs.get('g') == 'G90':
				# absolute coordinantes
				# this may do something in the program in the future if I support other modes of operations
				self.g = 'G90'
		elif linetype == 'XY':
			# TODO input handling to accept both int()s and ['Xint()', 'Yint()']
			# xy lines will have a movement type of g, x and y cords and may include a speed as f
			self.g = kwargs.get('g')
			self.x = kwargs.get('x')
			self.y = kwargs.get('y')
			if 'f' in kwargs.keys():
				self.f = kwargs.get('f')
		elif linetype == 'Z':
			# z lines will have a movement type of g, a z cord and may include a speed as f
			self.g = kwargs.get('g')
			self.z = kwargs.get('z')
			if 'f' in kwargs.keys():
				self.f = kwargs.get('f')
		elif linetype == 'M':
			# m lines control spindle state/speed or laser state/power level. speed/power is optional as s
			self.m = kwargs.get('m')
			if 's' in kwargs.keys():
				self.s = kwargs.get('s')
		else:
			# TODO add help information
			linetypes = ['comment', 'G', 'XY', 'Z', 'M']
			raise TypeError(f'linetype is required, supported line types are {linetypes}')

	def __repr__(self):
		# TODO test that this returns a properly formatted line
		p = []
		if hasattr(self, 'fln'):
			p.append(self.fln)
		if self.type == 'comment':
			p.append(self.comment)
		if self.type == 'G':
			p.append(self.g)
		if self.type == 'XY':
			p.append(self.g)
			p.append('X' + self.x)
			p.append('Y' + self.y)
			if hasattr(self, 'f'):
				p.append('F' + self.f)
		if self.type == 'Z':
			p.append(self.g)
			p.append(self.z)
			if hasattr(self, 'f'):
				p.append(self.f)
		if self.type == 'M':
			p.append(self.m)
			if hasattr(self, 's'):
				p.append(self.s)
		return print(*p)

	def xy(self, xy=''):
		if self.type == 'XY':
			if type(xy) == list and len(xy) == 2:
				self.x = xy[0]
				self.y = xy[1]
			elif xy == '':
				r = [float(self.x), float(self.y)]
				return r
			else:
				raise TypeError('list of two floats expected as argument to modify xy values')

		else:
			raise TypeError(f'you can not call XY operations on a line of type {self.type}')

	def z(self, z=''):
		if self.type == 'Z':
			if type(z) == float:
				self.z = z
			elif z == '':
				r = float(self.z)
				return r
			else:
				raise TypeError('float expected as argument to modify z value')
		else:
			raise TypeError(f'you can not call Z operations on a line of type {self.type}')

	def typechange(self, newtype, **kwargs):
		supportedlines = ['Z', 'M']
		if any(i in self.type for i in supportedlines):
			if newtype == 'M':
				for j in ['z', 'f', 's']:
					delattr(self, j)
				self.type = 'M'
				self.m = kwargs.get('m')
				if 's' in kwargs.keys():
					self.s = kwargs.get('s')

			elif newtype == 'Z':
				for j in ['m', 's', 'f']:
					delattr(self, j)
				self.type = 'Z'
				self.z = kwargs.get('z')
				if 'f' in kwargs.keys():
					self.f = kwargs.get('f')

			else:
				raise TypeError('supported new types are M or Z')
		else:
			raise TypeError(f'this module can only be used on lines of type {supportedlines}')

	def fln(self, newfln=''):
		if newfln == '':
			if hasattr(self, 'fln'):
				return self.fln
			else:
				raise LookupError('seems we dont have a line number to give you chief')
		elif newfln[0] == 'N' and int(newfln[1:]):
			self.fln = newfln
		else:
			raise IOError(f'this module can be used to get or set a file line number in format "Nxxx"')



class Gmove:


	def __init__(self, type, glines):
		# expects a type of move or "line block", i.e. comments at the begining of the file including setup info
		# types expected are ['header', 'move', 'footer'] and glines is a list of gline() objects
		#TODO determine if this is the types we want, also consider what would be required to support tool changes
		self.type = type
		self.lines = glines

	def __repr__(self):
		p = []
		q = ['type', self.type]
		p.append(q)
		q = ['length', self.len()]
		p.append(q)
		q = ['start XY', self.startxy()]
		p.append(q)
		return p

	def __len__(self):
		return len(self.lines)

	def startxy(self):
		for i in self.lines:
			if i.type == 'XY':
				return i.xy()

	def fullxy(self, newxy=''):
		# returns the full xy list as a list[[x, y], [x, y]]
		# if supplied with newxy in the same format as returned
		# by this function when called without arguments it will update the xy moves with the new values
		#TODO these are wild claims which have not been evaluated by any testing body
		l = []
		if newxy == '':
			for i in self.lines:
				if i.type == 'XY':
					l.append(i.xy())
			return l
		elif type(newxy) == list:
			#TODO this indexing is broken, it is not considering non-xy line types, this needs added
			if len(newxy) == len(self):
				for i in range(len(self)):
					self.lines[i].xy(newxy[i])
					# holy shit this will be cool if it works as expected
			else:
				raise IndexError(f'')
		else:
			raise TypeError(f'')



class Gfile:


	def __init__(self, type, gmoves):
		# supported 'type' = ['etch', 'drill', 'screen']
		# gmoves expected as a list[] of gmove() objects
		self.type = type
		self.moves = gmoves

	def __repr__(self):
		p = []
		q = ['type', self.type]
		p.append(q)
		q = ['number of moves', self.len()]
		p.append(q)
		r = 0
		for i in self.moves:
			r = r + i.len()
		q = ['total number of lines', r]
		p.append(q)
		return p

	def __len__(self):
		return len(self.moves)

	def movelist(self, newmoves=''):
		# newmoves optional, expected as a list of lists in the same format as
		# returned by this function when called without arguments: [[[x, y],[x, y]],[[x, y],[x, y]]]
		if newmoves == '':
			p = []
			for i in self.moves:
				p.append(i.fullxy())
			return p
		elif type(newmoves) == list:
			if len(newmoves) == len(self):
				for i in range(len(self)):
					self.moves[i].fullxy(newxy=newmoves[i])

	def movestart(self):
		# returns a list of the start xy for each in the format [['index', 'type', '[x,y]'], ...]
		p = []
		c = 0
		for i in self.moves:
			p.append([c, i.type, i.startxy()])
			c = c + 1
		return p

	def moveshuffle(self, newmoves):
		# expects a list of index numbers for the new move order, len(newmoves) must match len(self)
		# format should be [6, 4, 7, 2, 3, 1, 5, 8, 9]
		if len(newmoves) == len(self):
			shufflemoves = []
			for i in newmoves:
				shufflemoves.append(self.moves[i])
			self.moves = shufflemoves
