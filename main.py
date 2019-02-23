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

			self.field_p = NamedTextbox(self.frame_input, text = "p", state = "readonly")
			self.field_p.pack(pady = 5)

			self.field_q = NamedTextbox(self.frame_input, text = "q", state = "readonly")
			self.field_q.pack()

			self.field_phi = NamedTextbox(self.frame_input, text = "phi", state = "readonly")
			self.field_phi.pack(pady = 5)

			self.field_k = NamedTextbox(self.frame_input, text = "k", state = "readonly")
			self.field_k.pack()

			self.field_u0 = NamedTextbox(self.frame_input, text = "u0", state = "readonly")
			self.field_u0.pack(pady = 5)

			self.button_generate = Button(self.frame_input, text = "Сгенерировать", command = self.action)
			self.button_generate.pack()

			# Блок вывода результата генерирования
			#self.frame_output = Frame(self)
			#self.frame_output.grid(row = 0, column = 1, padx = 5)

			# Содержимое блока
			self.result = Text(self, width = 30, height = 11, state = "disabled")
			self.result.pack(side = LEFT)

		def action(self):
			m = self.field_m.get()
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

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("RSA генератор")
		self.resizable(False, False)
		self.geometry("%dx%d" % (500, 300))

		self.frame_root = Frame(self)
		self.frame_root.pack(expand = YES, fill = BOTH)

		self.frame_generator = self.generator(self.frame_root)
		self.frame_generator.pack(padx = 5, ipadx = 5, ipady = 10)

		#self.frame_frequency = self.frequency(self.frame_root)
		#self.frame_frequency.pack(padx = 5, pady = 5, ipadx = 5, ipady = 10)

if __name__ == "__main__": app().mainloop()