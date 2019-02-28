from random import randint

def gcd(a, b):
	# Алгоритм Евклида (НОД)
	while b != 0:
		c = a % b
		a = b
		b = c
	return abs(a)

def legendre(str):
	# Вычисление символа Лежандра
	# Какойто алгоритм на разложении на сомножители из интернетов
	# https://www.easycalculation.com/legendre-symbol.php
	noNeg = str[0]
	nme = str[1]
	dnm = str[2]

	nme %= dnm
	if nme == 0:
		return 0
	
	if nme == 1:
		if noNeg > 0:
			return 1
		else:
			return -1
	
	syinc = 1
	if 3 == dnm % 8 or 5 == dnm % 8:
		syinc = -1
	
	lstary = [ 1 ] * 3
	if 0 == nme % 2:
		lstary[0] = syinc * noNeg
		lstary[1] = nme // 2
		lstary[2] = dnm
		return legendre(lstary)

	if 3 == dnm % 4 and 3 == nme % 4:
		lstary[0] = -noNeg
		lstary[1] = dnm % nme
		lstary[2] = nme
		return legendre(lstary)
	else:
		lstary[0] = noNeg
		lstary[1] = dnm % nme
		lstary[2] = nme
		return legendre(lstary)

def solovay_strassen(n, k = 3):
	# Проверка числа на простоту используя тест Соловея-Штрассена
	for _ in range(k):
		a = randint(2, n - 1)
		if gcd(a, n) != 1 or pow(a, (n - 1) // 2, n) - legendre([ 1, a, n ]) % n != 0:
			return False
	return True # Вероятность 1 - 2 ^ (-k)

def genbits(n):
	# Генерируем псевдослучайную последовательность бит (какойто алгоритм из крипты за 5 семак)
	res = 1
	for _ in range(n - 1):
		res <<= 1
		res += randint(0, 1)
	res <<= 1
	res += 1
	return res

def genprime(m):
	# Генератор простых чисел
	while True:
		num = genbits(m)
		if solovay_strassen(num):
			return num

def generate(m, p, q, k, u0):
	# Проверки 1
	if not solovay_strassen(p):
		raise ValueError("p")
	if not solovay_strassen(q) or q == p:
		raise ValueError("q")
	# Вспомогательные переменные
	N = p * q
	phi = (p - 1) * (q - 1)
	# Проверки 2
	if not (1 < k < phi and gcd(k, phi) == 1):
		raise ValueError("k")
	if not (1 < u0 < N - 1):
		raise ValueError("u0")
	# Генерация последовательности
	x = list(); u = [ u0 ]
	for _ in range(m):
		u.append(pow(u[-1], k, N))
		x.append(u[-1] & 0x1)
	return "".join(map(str, x))
