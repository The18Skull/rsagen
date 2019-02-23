from tkinter import *
from tkinter import ttk

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

			# Блок ввода параметров генератора
			self.frame_input = Frame(self)
			self.frame_input.pack(side = LEFT, padx = 5)

			# Содержимое блока
			self.field_m = NamedTextbox(self.frame_input, text = "m", state = "normal")
			self.field_m.pack()

			self.button_generate = Button(self.frame_input, text = "Сгенерировать", command = self.action)
			self.button_generate.pack(pady = 5)

			self.field_p = NamedTextbox(self.frame_input, text = "p", state = "readonly")
			self.field_p.pack()

			self.field_q = NamedTextbox(self.frame_input, text = "q", state = "readonly")
			self.field_q.pack(pady = 5)

			self.field_phi = NamedTextbox(self.frame_input, text = "phi", state = "readonly")
			self.field_phi.pack()

			self.field_k = NamedTextbox(self.frame_input, text = "k", state = "readonly")
			self.field_k.pack(pady = 5)

			self.field_u0 = NamedTextbox(self.frame_input, text = "u0", state = "readonly")
			self.field_u0.pack()

			# Блок вывода результата генерирования
			#self.frame_output = Frame(self)
			#self.frame_output.grid(row = 0, column = 1, padx = 5)

			# Содержимое блока
			self.result = Text(self, width = 30, height = 11, state = "disabled")
			self.result.pack(side = LEFT)

		def action(self):
			m = self.field_m.get()
			self.master.master.frame_frequency.put(1, 2)
			# TODO: generator func

		def put(self, text):
			self.result.config(state = "normal")
			self.result.delete("0.0", END)
			self.result.insert("0.0", text)
			self.result.config(state = "disabled")

	class frequency(LabelFrame):
		def __init__(self, *args, **kwargs):
			kwargs["text"] = "Частотный тест"
			super().__init__(*args, **kwargs)

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
			kwargs["text"] = "Расширенный тест на\nпроизвольные отклонения"
			super().__init__(*args, **kwargs)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("RSA генератор")
		self.resizable(False, False)
		self.geometry("%dx%d" % (500, 500))

		self.frame_root = Frame(self)
		self.frame_root.pack(expand = YES, fill = BOTH)

		self.frame_generator = self.generator(self.frame_root)
		self.frame_generator.pack(padx = 5, ipadx = 5, ipady = 10)

		self.frame_frequency = self.frequency(self.frame_root)
		self.frame_frequency.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

		self.frame_sequence = self.sequence(self.frame_root)
		self.frame_sequence.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

if __name__ == "__main__": app().mainloop()