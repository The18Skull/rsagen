import re
import rsa
from tkinter import *
from tkinter import messagebox

class NamedTextbox(Frame):
	def __init__(self, *args, **kwargs):
		self.text = kwargs["text"] # text in lable
		self.state = kwargs["state"] if "state" in kwargs else "normal" # state of entry (normal, readonly, disabled)
		kwargs.clear()
		super().__init__(*args, **kwargs)

		self.label = Label(self, width = 5, text = self.text) # width - width in chars
		self.label.pack(side = LEFT)

		self.entry = Entry(self, justify = CENTER, state = self.state) # width - width in chars
		self.entry.pack(side = LEFT, expand = YES, fill = X)
	
	def get(self):
		return self.entry.get()
	
	def put(self, text):
		self.entry.config(state = "normal")
		self.entry.delete(0, END)
		self.entry.insert(0, text)
		self.entry.config(state = self.state)

class StatisticOutput(NamedTextbox):
	def __init__(self, *args, **kwargs):
		#kwargs["fieldbackground"] = [ ( "readonly", "lime" ), ( "disabled", "red" ) ]
		super().__init__(*args, **kwargs)

	def put(self, val):
		self.entry.config(state = "normal")
		self.entry.delete(0, END)
		self.entry.insert(0, val)
		#self.entry.config(bg = ("lime" if val <= 1.82 else "red"))
		self.entry.config(readonlybackground = ("lime" if val <= 1.82138636 else "red"))
		self.entry.config(state = "readonly")

class app(Tk):
	class generator(LabelFrame):
		def __init__(self, *args, **kwargs):
			kwargs["text"] = "RSA генератор"
			super().__init__(*args, **kwargs)
			self.root = self.master.root

			# Блок ввода параметров генератора
			self.frame_input = Frame(self)
			self.frame_input.pack()

			self.frame_left = Frame(self.frame_input)
			self.frame_left.pack(side = LEFT)

			self.frame_right = Frame(self.frame_input)
			self.frame_right.pack(side = LEFT)

			# Содержимое блока
			self.field_m = NamedTextbox(self.frame_left, text = "m", state = "normal")
			self.field_m.pack()

			self.field_p = NamedTextbox(self.frame_left, text = "p", state = "normal")
			self.field_p.pack(pady = 5)

			self.field_q = NamedTextbox(self.frame_left, text = "q", state = "normal")
			self.field_q.pack()

			#self.field_phi = NamedTextbox(self.frame_input, text = "phi", state = "normal")
			#self.field_phi.pack()

			self.field_k = NamedTextbox(self.frame_right, text = "k", state = "normal")
			self.field_k.pack(pady = 5)

			self.field_u0 = NamedTextbox(self.frame_right, text = "u0", state = "normal")
			self.field_u0.pack()

			self.button_generate = Button(self, text = "Сгенерировать", command = self.action)
			self.button_generate.pack(pady = 5)

			# Блок вывода результата генерирования
			self.result = Text(self, width = 40, height = 9, state = "normal")
			self.result.bind("<KeyRelease>", self.calcStat)
			self.result.pack()

		def action(self):
			# Генератор
			# m
			m = self.field_m.get()
			if not m:
				m = rsa.randint(10, 10000)
				self.field_m.put(m)
				return
			else:
				m = int(m)
			# p
			p = self.field_p.get()
			if not p:
				p = rsa.genprime(32)
				self.field_p.put(p)
			else:
				p = int(p)
			if not rsa.solovay_strassen(p):
				messagebox.showerror("Ошибка", "Число p не простое")
			# q
			q = self.field_q.get()
			if not q:
				q = rsa.genprime(32)
				self.field_q.put(q)
			else:
				q = int(q)
			if not rsa.solovay_strassen(q) or q == p:
				messagebox.showerror("Ошибка", "Число q не простое")
			# k
			phi = (p - 1) * (q - 1)
			k = self.field_k.get()
			if not k:
				while rsa.gcd(k, phi) != 1:
					k = rsa.randint(2, phi - 1)
				self.field_k.put(k)
			else:
				k = int(k)
			if not (1 < k < phi and rsa.gcd(k, phi) == 1):
				messagebox.showerror("Ошибка", "Некорректное значение k (1 < k < %d и НОД(k, %d))" % (phi, phi))
			# u0
			N = p * q
			u0 = self.field_u0.get()
			if not u0:
				u0 = rsa.randint(2, N - 2)
				self.field_u0.put(u0)
			else:
				u0 = int(u0)
			if not (1 < u0 < N - 1):
				messagebox.showerror("Ошибка", "Некорректное значение u0 (1 < u0 < %d)" % (N - 1))
			seq = rsa.generate(m, p, q, k, u0)
			self.put(seq)
			#self.calcStat()

		def calcStat(self, ev = None):
			# Посчитать значения статистик
			text = self.get() # текущее содержание поля с выводом последовательности
			if re.search(r"[^01]", text) is not None:
				messagebox.showerror("Ошибка", "В поле ввода должны быть только 0 и 1")
				text = re.sub(r"[^01]", "", text)
				self.put(text)
				return
			#print(text)
			self.root.frame_frequency.put(1, 2)
			self.root.frame_sequence.put(1, 1, 1)
			self.root.frame_deviation.put([ 1 ] * 19, [ 1 ] * 19)

		def get(self):
			# Получить содержимое поля вывода последовательности
			return self.result.get("0.0", END)[:-1]

		def put(self, text):
			# Заменить текст в поле вывода последовательности
			#self.result.config(state = "normal")
			self.result.delete("0.0", END)
			self.result.insert("0.0", text)
			#self.result.config(state = "disabled")

	class frequency(LabelFrame):
		def __init__(self, *args, **kwargs):
			kwargs["text"] = "Частотный тест"
			super().__init__(*args, **kwargs)
			self.root = self.master.root

			# Содержимое блока
			self.field_sn = NamedTextbox(self, text = "Sn", state = "readonly")
			self.field_sn.pack(pady = 5)

			self.field_s = StatisticOutput(self, text = "S", state = "readonly")
			self.field_s.pack()

		def put(self, sn, s):
			# Установить поля Sn и S одной командой
			self.field_sn.put(sn)
			self.field_s.put(s)

	class sequence(LabelFrame):
		def __init__(self, *args, **kwargs):
			kwargs["text"] = "Тест на последовательность\nодинаковых бит"
			super().__init__(*args, **kwargs)
			self.root = self.master.root

			# Содержимое блока
			self.field_pi = NamedTextbox(self, text = "pi", state = "readonly")
			self.field_pi.pack(pady = 5)

			self.field_vn = NamedTextbox(self, text = "Vn", state = "readonly")
			self.field_vn.pack()

			self.field_s = StatisticOutput(self, text = "S", state = "readonly")
			self.field_s.pack(pady = 5)

		def put(self, pi, vn, s):
			# Установить поля pi, Vn и S одной командой
			self.field_pi.put(pi)
			self.field_vn.put(vn)
			self.field_s.put(s)

	class deviation(LabelFrame):
		def __init__(self, *args, **kwargs):
			kwargs["text"] = "Расширенный тест на произвольные отклонения"
			super().__init__(*args, **kwargs)
			self.root = self.master.root

			self.fields_ksi = list()
			self.fields_y = list()
			for i in range(18):
				j = i - 9
				if j >= 0:
					j += 1
				self.fields_ksi.append(NamedTextbox(self, text = ("ksi[%d]" % j), state = "readonly"))
				self.fields_ksi[-1].grid(row = i, column = 0, pady = (5 if i % 2 == 0 else 0))
				self.fields_y.append(StatisticOutput(self, text = ("Y[%d]" % j), state = "readonly"))
				self.fields_y[-1].grid(row = i, column = 1, pady = (5 if i % 2 == 0 else 0))

		def put(self, ksi, Y):
			# Установить поля ksi и Y одной командой
			for i in range(18):
				self.fields_ksi[i].put(ksi[i])
				self.fields_y[i].put(Y[i])

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("RSA генератор")
		self.resizable(False, False)
		self.geometry("%dx%d" % (700, 550))

		self.frame_root = Frame(self)
		self.frame_root.pack(expand = YES, fill = BOTH)
		self.frame_root.root = self

		self.frame_left = Frame(self.frame_root)
		self.frame_left.pack(side = LEFT)
		self.frame_left.root = self

		self.frame_generator = self.generator(self.frame_left)
		self.frame_generator.pack(padx = 5, pady = 5, ipadx = 5, ipady = 10)

		self.frame_frequency = self.frequency(self.frame_left)
		self.frame_frequency.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

		self.frame_sequence = self.sequence(self.frame_left)
		self.frame_sequence.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

		self.frame_right = Frame(self.frame_root)
		self.frame_right.pack(side = LEFT)
		self.frame_right.root = self

		self.frame_deviation = self.deviation(self.frame_right)
		self.frame_deviation.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

if __name__ == "__main__": app().mainloop()