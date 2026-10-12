class Life:
	@classmethod
	def init(cls, lst, height, width, dy, dx):
		obj = Life()
		obj.lst = lst
		obj.height = height
		obj.width = width
		obj.dy = dy
		obj.dx = dx
		return obj
	@classmethod
	def init_rle(cls, s):
		t = s.split('\n')
		s = '\n'.join(t[1:])
		k = t[0].split(',')
		lst_params = [[l.strip() for l in j.strip().split('=')] for j in k]
		dict_ = {}
		for i, j in lst_params:
			dict_[i] = j
		x = int(dict_['x'])
		y = int(dict_['y'])
		s1 = ''
		i = 0
		while i < len(s):
			if s[i] == 'o':
				s1 += 'o'
			elif s[i] == 'b':
				s1 += 'b'
			elif s[i] == '$':
				s1 += '$'
			elif s[i] == '\n':
				pass
			elif '0' <= s[i] <= '9':
				s2 = ''
				j = i
				while j < len(s) and '0' <= s[j] <= '9':
					j += 1
				s2 = s[i:j]
				s1 += s[j] * int(s2)
				i += len(s2)
			i += 1
		lst = [[0] * x for i in range(y)]
		i = 0
		j = 0
		for c in s1:
			if c == 'o':
				lst[i][j] = 1
				j += 1
			elif c == 'b':
				j += 1
			elif c == '$':
				i += 1
				j = 0
		return Life(lst, y, x)
	def to_rle(self):
		s = ''
		s += f'x = {self.width}, y = {self.height}, rule = B23/S3\n'
		for i in self.lst:
			for j in i:
				if j == 1:
					s += 'o'
				else:
					s += 'b'
			s += '$\n'
		return s
	def __init__(self, lst=None, height=10, width=10, dy=0, dx=0):
		self.height = height
		self.width = width
		if lst != None:
			self.lst = [i[:] for i in lst]
		else:
			self.lst = [
				[0] * width
				for i in range(height)
			]
		assert self.height == len(self.lst)
		self.dx = dx
		self.dy = dy
	def count(self):
		c = 0
		for i in self.lst:
			for j in i:
				c += j
		return c
	def add_glider(self, x, y, s=0):
		if s == 0:
			g = '111/001/010'
		elif s == 1:
			g = '001/101/011'
		elif s == 2:
			g = '010/100/111'
		elif s == 3:
			g = '110/101/100'
		elif s == 4:
			g = '111/100/010'
		elif s == 5:
			g = '011/101/001'
		elif s == 6:
			g = '010/001/111'
		elif s == 7:
			g = '100/101/110'
		g = g.split('/')
		g = [[int(i) for i in s] for s in g]
		for i in range(3):
			for j in range(3):
				self._set_cell_(x + i, y + j, g[i][j])
	def extend_y(self, height, flag='>'):
		if flag == '>':
			self.lst += [
				[0] * self.width
				for i in range(height)
			]
			self.height += height
		else:
			self.lst = [
				[0] * self.width
				for i in range(height)
			] + self.lst
			self.height += height
			self.dy += height
	def extend_x(self, width, flag='>'):
		if flag == '>':
			for i in range(self.height):
				self.lst[i] += [0] * width
			self.width += width
		else:
			for i in range(self.height):
				self.lst[i] = [0] * width + self.lst[i]
			self.width += width
			self.dx += width
	def _get_cell(self, y, x):
		y_ = y + self.dy
		x_ = x + self.dx
		if 0 <= y_ < self.height and 0 <= x_ < self.width:
			return self.lst[y_][x_]
		else:
			return None
	def _set_cell(self, y, x, val):
		y_ = y + self.dy
		x_ = x + self.dx
		if 0 <= y_ < self.height and 0 <= x_ < self.width:
			self.lst[y_][x_] = val
			return True
		else:
			return False
	def _get_cell_(self, y, x):
		y_ = y + self.dy
		x_ = x + self.dx
		if 0 <= y_ < self.height and 0 <= x_ < self.width:
			return self.lst[y_][x_]
		else:
			return 0
	def _set_cell_(self, y, x, val):
		y_ = y + self.dy
		x_ = x + self.dx
		if 0 <= y_ < self.height and 0 <= x_ < self.width:
			self.lst[y_][x_] = val
			return True
		else:
			if val == 0:
				return True
			else:
				while y + self.dy < 0:
					self.extend_y(1, '<')
				while y + self.dy >= self.height:
					self.extend_y(1, '>')
				while x + self.dx < 0:
					self.extend_x(1, '<')
				while x + self.dx >= self.width:
					self.extend_x(1, '>')
				self.lst[y + self.dy][x + self.dx] = val
				return True
	def play(self):
		lst1 = [[0] * (self.width + 2) for i in range(self.height + 2)]
		for i in range(self.height + 2):
			for j in range(self.width + 2):
				I = i - 1
				J = j - 1
				C = 0
				for i_ in range(-1, 2):
					for j_ in range(-1, 2):
						if i_ or j_:
							c = self._get_cell(I - self.dy + i_, J - self.dx + j_) or 0
							C += c
				c_ = self._get_cell(I - self.dy, J - self.dx) or 0
				if c_ == 0 and C == 3 or c_ == 1 and C in (2, 3):
					lst1[i][j] = 1
				else:
					lst1[i][j] = 0
		self.lst = lst1
		self.dy += 1
		self.dx += 1
		self.height += 2
		self.width += 2
		while self.height and sum(self.lst[0]) == 0:
			self.lst = self.lst[1:]
			self.dy -= 1
			self.height -= 1
		while self.height and sum(self.lst[-1]) == 0:
			self.lst = self.lst[:-1]
			self.height -= 1
		while self.width and sum([i[0] for i in self.lst]) == 0:
			self.lst = [i[1:] for i in self.lst]
			self.dx -= 1
			self.width -= 1
		while self.width and sum([i[-1] for i in self.lst]) == 0:
			self.lst = [i[:-1] for i in self.lst]
			self.width -= 1
	def __repr__(self):
		return f'Life.init({self.lst}, {self.height}, {self.width}, {self.dy}, {self.dx})'
	def __str__(self):
		s = f'Life.init({self.lst}, {self.height}, {self.width}, {self.dy}, {self.dx})\n'
		for i in range(-25, 26):
			for j in range(-25, 26):
				c = self._get_cell(i, j)
				if c == 1:
					s += '+'
				elif c == 0:
					s += '-'
				else:
					s += '/'
			s += '\n'
		s += '\n'
		return s

for y1 in range(-15, 5):
	for x1 in range(10, 15):
		for y2 in range(15, 25):
			for x2 in range(-15, 5):
				l = Life.init_rle('''x = 6, y = 6, rule = B3/S23
bo$obo$bobo$2bobo$3bobo$4bo''')
				l.add_glider(y1, x1, 2)
				l.add_glider(y2, x2, 0)
				rle = l.to_rle()
				c_ = 0
				for i in range(500):
					l.play()
					if l.count() == 0:
						print(rle)
						exit(0)
