from math import sqrt

def transform(seq):
	# Преобразовать последовательность из 0 и 1 в последовательность из -1 и 1
	return [ 2 * int(x) - 1 for x in seq ]

def frequency(seq):
	# Частотный тест
	seq = transform(seq) # 1
	Sn = sum(seq) # 2
	S = abs(Sn) / (len(seq) ** 0.5) # 3
	return Sn, S

def sequence(seq):
	# Тест на последовательность одинаковых бит
	n = len(seq)
	seq = [ int(x) for x in seq ]
	pi = sum(seq) / n # 1
	Vn = 1 + sum([ 0 if seq[i] == seq[i + 1] else 1 for i in range(n - 1) ]) # 2
	S = abs(Vn - 2 * n * pi * (1 - pi)) / (2 * sqrt(2 * n) * pi * (1 - pi)) # 3
	return pi, Vn, S

def deviation(seq):
	# Расширенный тест на произвольные отклонения
	seq = transform(seq) # 1
	S = [ seq[0] ]
	for i in range(1, len(seq)): # 2
		S.append(seq[i] + S[-1])
	L = S.count(0) + 1
	ksi = list(); Y = list()
	for i in range(19):
		if i == 9: continue
		ksi.append(S.count(i - 9))
		Y.append(abs(ksi[-1] - L) / sqrt(2 * L * (4 * abs(i - 9) - 2)))
	return ksi, Y