class Stack:
	def __init__(self):
		self.elements = []

	def push(self, value):
		self.elements.insert(0, value)

	def rotate(self):
		if self.elements:
			self.elements.append(self.elements.pop(0))

	def reverse_rotate(self):
		if self.elements:
			self.elements.insert(0, self.elements.pop())

	def swap(self):
		if len(self.elements) > 1:
			self.elements[0], self.elements[1] = self.elements[1], self.elements[0]	

	def pop(self):
		return self.elements.pop(0) if self.elements else None

	def size(self):
		return len(self.elements)

	def clear(self):
		self.elements = []