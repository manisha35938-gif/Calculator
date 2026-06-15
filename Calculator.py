"""
Simple GUI Calculator

This file implements a professional, user-friendly calculator application
implemented with Tkinter. It follows clean coding practices and includes:
 - Addition, Subtraction, Multiplication, Division, Percentage
 - Decimal calculations
 - Clear and Backspace
 - Division-by-zero protection and input validation
 - Keyboard bindings for Enter, Backspace and Escape

This implementation was created to satisfy a CRAFT-style prompt for a
beginner-friendly, extensible calculator application (Python 3.8+).
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def safe_eval(expression: str) -> str:
	"""Evaluate a mathematical expression safely for this calculator.

	Only allow digits, parentheses, operators and dot. Replace percentage
	with division by 100. Returns result as string or raises ValueError on
	invalid input. Raises ZeroDivisionError for division by zero.
	"""
	allowed = set("0123456789.+-*/()% ")
	if not expression:
		return ""
	if any(ch not in allowed for ch in expression):
		raise ValueError("Invalid characters in expression")

	# support percent: convert occurrences like '50%' -> '(50/100)'
	# We use a simple transform that replaces '%' with '/100'. This keeps
	# the parsing straightforward for the small calculator grammar.
	expr = ''
	i = 0
	while i < len(expression):
		ch = expression[i]
		if ch == '%':
			# replace lone % with '/100'
			expr += '/100'
			i += 1
			continue
		expr += ch
		i += 1

	# Prevent dangerous patterns (double-operator power or integer divide not allowed)
	if '**' in expr or '//' in expr:
		raise ValueError('Unsupported operator')

	# Evaluate using Python's eval in restricted globals
	try:
		result = eval(expr, { }, { })
	except ZeroDivisionError:
		raise ZeroDivisionError('Division by zero')
	except Exception:
		raise ValueError('Malformed expression')

	# Format result: show integer without decimal point when possible
	if isinstance(result, float) and result.is_integer():
		result = int(result)
	return str(result)


class Calculator(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('Calculator')
		self.resizable(False, False)
		self.configure(padx=8, pady=8)

		self.expression = tk.StringVar()

		self._create_widgets()

	def _create_widgets(self):
		# Display
		entry = ttk.Entry(self, textvariable=self.expression, font=('Segoe UI', 18), justify='right')
		entry.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=(0, 8))
		entry.focus()

		# Button layout
		buttons = [
			('C', 1, 0, self.clear), ('⌫', 1, 1, self.backspace), ('%', 1, 2, lambda: self._add('%')), ('/', 1, 3, lambda: self._add('/')),
			('7', 2, 0, lambda: self._add('7')), ('8', 2, 1, lambda: self._add('8')), ('9', 2, 2, lambda: self._add('9')), ('*', 2, 3, lambda: self._add('*')),
			('4', 3, 0, lambda: self._add('4')), ('5', 3, 1, lambda: self._add('5')), ('6', 3, 2, lambda: self._add('6')), ('-', 3, 3, lambda: self._add('-')),
			('1', 4, 0, lambda: self._add('1')), ('2', 4, 1, lambda: self._add('2')), ('3', 4, 2, lambda: self._add('3')), ('+', 4, 3, lambda: self._add('+')),
			('0', 5, 0, lambda: self._add('0')), ('.', 5, 1, lambda: self._add('.')), ('=', 5, 2, self.calculate),
		]

		for (txt, r, c, cmd) in buttons:
			if txt == '=':
				btn = ttk.Button(self, text=txt, command=cmd)
				btn.grid(row=r, column=c, columnspan=2, sticky='nsew', padx=4, pady=4)
			else:
				btn = ttk.Button(self, text=txt, command=cmd)
				btn.grid(row=r, column=c, sticky='nsew', padx=4, pady=4)

		# Configure grid weights for responsiveness
		for i in range(6):
			self.rowconfigure(i, weight=1)
		for j in range(4):
			self.columnconfigure(j, weight=1)

		# Keyboard bindings
		self.bind('<Return>', lambda e: self.calculate())
		self.bind('<BackSpace>', lambda e: self.backspace())
		self.bind('<Escape>', lambda e: self.clear())

	def _add(self, char: str):
		# Append character to expression
		self.expression.set(self.expression.get() + char)

	def clear(self):
		self.expression.set('')

	def backspace(self):
		self.expression.set(self.expression.get()[:-1])

	def calculate(self):
		expr = self.expression.get()
		try:
			result = safe_eval(expr)
		except ZeroDivisionError:
			messagebox.showerror('Error', 'Division by zero')
			return
		except Exception:
			messagebox.showerror('Error', 'Invalid expression')
			return
		self.expression.set(result)


if __name__ == '__main__':
	app = Calculator()
	app.mainloop()
