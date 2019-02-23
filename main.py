from tkinter import *
from tkinter import ttk

class app(Tk):
	class generator(LabelFrame):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title("RSA генератор")
		self.geometry("%dx%d" % (400, 600))

		self.frame_root = Frame(self)
		self.frame_root.pack(expand = YES, fill = BOTH)

		self.frame_generator = self.generator(self.frame_root, text = "RSA генератор")
		self.frame_generator.pack(expand = YES, fill = BOTH, padx = 5, ipadx = 5)

if __name__ == "__main__": app().mainloop()