class Board:
	N = 3

	def __init__(self, initial_symbol):
		self.data = [[initial_symbol for _ in range(Board.N)] for _ in range(Board.N)]
		self.initial_symbol = initial_symbol


	# 現在の盤面の表示
	def display(self):
		# 盤面の中身
		results = [''.join(row) for row in self.data]
		# 盤面の縁←
		results = [str(i) + r for i, r in enumerate(results, 1)]
		# 盤面の縁↑
		results.insert(0, ' ' + ''.join([str(i) for i in range(1, Board.N + 1)]))

		# 描画
		for r in results:
			print(r)


	# 盤面に印をつける
	def set(self, x, y, symbol):
		self.data[y - 1][x - 1] = symbol

	# 盤面情報を取得
	def get(self, x, y):
		return self.data[y - 1][x - 1]


	# 添え字が盤面の範囲内か
	def is_range(self, x, y):
		xr = 1 <= x <= Board.N
		yr = 1 <= y <= Board.N
		return xr and yr


	# 盤面が埋まったか
	def check_fill(self):
		return not any([any([c == self.initial_symbol for c in row]) for row in self.data])


	# 任意の文字が任意の数連続しているかを確認

	# 任意の文字配列の中で
	def check(self, line, symbol, number):
		line_str = ''.join(line)
		target = ''.join([symbol for _ in range(number)])
		return target in line_str

	# 行の中で
	def check_rows(self, symbol, number):
		return any([self.check(row, symbol, number) for row in self.data])

	# 列の中で
	def check_columns(self, symbol, number):
		columns = [[self.data[y][x] for y in range(len(self.data))] for x in range(len(self.data[0]))]
		return any([self.check(column, symbol, number) for column in columns])

	# ななめの中で
	def check_diagonal_lines(self, symbol, number):
		# とりあえず一番長いとこだけ実装
		diagonal_line_1 = [self.data[i][i] for i in range(Board.N)]
		diagonal_line_2 = [self.data[Board.N - 1 - i][i] for i in range(Board.N)]
		return any([self.check(dia, symbol, number) for dia in [diagonal_line_1, diagonal_line_2]])

	# 盤面全体の中で
	def check_all(self, symbol, number):
		if self.check_rows(symbol, number):
			return True
		elif self.check_columns(symbol, number):
			return True
		elif self.check_diagonal_lines(symbol, number):
			return True
		else:
			return False


FREE = '-'
O = 'o'
X = 'x'

b = Board(FREE)
turn = O

while True:
	b.display()
	print(f'{turn}の番です。座標を入力してください → ', end = '')
	x, y = [int(c) for c in input().split()]

	# 入力が正しいか確認
	if not b.is_range(x, y):
		print('範囲外です。再度入力してください。')
		continue
	
	if b.get(x, y) != FREE:
		print('既に印が付いています。再度入力してください。')


	b.set(x, y, turn)

	# 勝ったか確認
	if b.check_all(turn, Board.N):
		b.display()
		print(f'{turn}の勝ちです')
		break

	# 盤面が埋まったか確認
	if b.check_fill():
		b.display()
		print('引き分けです')
		break

	# 今の番を切り替え
	turn = O if turn != O else X

