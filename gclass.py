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
			# but we will keep their absolute position in the file as best we can
			self.comment = kwargs.get('comment')
		elif linetype == 'G':
			if kwargs.get('g') == 'G21':
				# metric mode
				# this may do something in the program in the future if I support other modes of operations
				self.g = 'G21'
			if kwargs.get('g') == 'G90':
				# absolute coordinantes
				# this may do something in the program in the future if I support other modes of operations
				self.g = 'G90'
		elif linetype == 'XY':
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
		p = []
		if hasattr(self, 'fln'):
			p.append(self.fln)
		if self.type == 'comment':
			p.append(self.comment)
		if self.type == 'G':
			p.append(self.g)
		if self.type == 'XY':
			p.append(self.g)
			p.append(self.x)
			p.append(self.y)
			if hasattr(self, 'f'):
				p.append(self.f)
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

	def XY(self, xy=''):
		if self.type == 'XY':
			if type(xy) == list and len(xy) = 2:
				self.x = xy[0]
				self.y = xy[1]
			if xy == '':
				r = [self.x, self.y]
				return r

		else:
			raise TypeError(f'you can not call XY operations on a line of type {self.type}')

	def

	def print(self):
		return
