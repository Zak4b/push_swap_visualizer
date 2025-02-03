#!/usr/bin/env python3

import tkinter as tk
from time import sleep
from stack import Stack
import random
import argparse
import subprocess

def reverse_operation(operation):
	if operation in ["sa", "sb", "ss"]:
		return operation
	if operation == "pa":
		return "pb"
	if operation == "pb":
		return "pa"
	if operation == "ra":
		return "rra"
	if operation == "rb":
		return "rrb"
	if operation == "rr":
		return "rrr"
	if operation == "rra":
		return "ra"
	if operation == "rrb":
		return "rb"
	if operation == "rrr":
		return "rr"

class PushSwapVisualizer:
	def __init__(self, root):
		self.root = root
		self.stack_a = Stack()
		self.stack_b = Stack()
		self.operations = []
		self.values = []
		self.operation_index = 0
		self.is_playing = False
		self.bar_height = None
		self.bar_config = None
		self.canvas = tk.Canvas(root, bg="white")
		self.canvas.pack(fill=tk.BOTH, expand=True)
		self.canvas_W = 0
		self.canvas_H = 0

		self.controls_frame = tk.Frame(root)
		self.controls_frame.pack()

		self.count_label = tk.Label(self.controls_frame, text="Number of elements:")
		self.count_label.pack(side=tk.LEFT)

		self.count_entry = tk.Entry(self.controls_frame, width=5)
		self.count_entry.pack(side=tk.LEFT)
		self.count_entry.insert(0, "10")

		self.generate_bt = tk.Button(self.controls_frame, text="Generate", command=self.generate_random_stack)
		self.generate_bt.pack(side=tk.LEFT)

		self.run_bt = tk.Button(self.controls_frame, text="Run Push Swap", command=self.run_push_swap)
		self.run_bt.pack(side=tk.LEFT)

		self.play_bt = tk.Button(self.controls_frame, text="⏯", command=self.play_visualization)
		self.play_bt.pack(side=tk.LEFT)

		self.forward_bt = tk.Button(self.controls_frame, text="Step Forward", command=self.step_forward)
		self.forward_bt.pack(side=tk.LEFT)

		self.backward_bt = tk.Button(self.controls_frame, text="Step Backward", command=self.step_backward)
		self.backward_bt.pack(side=tk.LEFT)

		self.number_label = tk.Label(root, textvariable=self.operation_index, font=("Arial", 20))
		self.number_label.pack(pady=20)

		self.speed_scale = tk.Scale(self.controls_frame, from_=1, to=100, orient=tk.HORIZONTAL, label="Speed")
		self.speed_scale.pack(side=tk.LEFT)
		self.speed_scale.set(5)

		self.text_frame = tk.Frame(root)
		self.text_frame.pack()

		self.input_label = tk.Label(self.text_frame, text="Input numbers:")
		self.input_label.pack(side=tk.LEFT)

		self.input_entry = tk.Entry(self.text_frame, width=50)
		self.input_entry.pack(side=tk.LEFT)

		self.operations_frame = tk.Frame(root)
		self.operations_frame.pack()

		self.operations_list = tk.Listbox(self.operations_frame, height=15, width=30)
		self.operations_list.pack()
		self.resize_job = None
		self.root.bind("<Configure>", self._resize)

	def _resize(self, event):
		if self.resize_job:
			self.root.after_cancel(self.resize_job) 
		self.resize_job = self.root.after(200, lambda: (self.calculate_bar_config(), self.draw_stacks()))

	def calculate_bar_config(self):
		self.canvas_W = self.canvas.winfo_width()
		self.canvas_H = self.canvas.winfo_height()
		max_elements = max(self.stack_a.size(), self.stack_b.size(), 1)
		self.bar_height = self.canvas_H / max_elements
		sorted_indices = {value: idx for idx, value in enumerate(sorted(self.stack_a.elements + self.stack_b.elements))}
		self.bar_config = {
			value: {
				"width": ((sorted_indices[value] + 1) / (len(sorted_indices))) * (self.canvas_W / 2),
				"color": f"#{int((sorted_indices[value] + 1) / len(sorted_indices) * 255):02x}00{255 - int((sorted_indices[value] + 1) / len(sorted_indices) * 255):02x}"
			}
			for value in sorted_indices
		}

	def draw_stacks(self):
		self.canvas.delete("all")
		self.draw_stack(self.stack_a, 0)
		self.draw_stack(self.stack_b, self.canvas_W / 2)

	def draw_stack(self, stack, x):
		y = 0
		for value in stack.elements:
			config = self.bar_config[value]
			self.canvas.create_rectangle(x, y, x + config["width"], y + self.bar_height, fill=config["color"], outline="")
			y += self.bar_height

	def execute_operation(self, operation):
		if operation == "pa":
			self.stack_a.push(self.stack_b.pop())
		elif operation == "pb":
			self.stack_b.push(self.stack_a.pop())
		elif operation == "sa":
			self.stack_a.swap()
		elif operation == "sb":
			self.stack_b.swap()
		elif operation == "ss":
			self.stack_a.swap()
			self.stack_b.swap()
		elif operation == "ra":
			self.stack_a.rotate()
		elif operation == "rb":
			self.stack_b.rotate()
		elif operation == "rr":
			self.stack_a.rotate()
			self.stack_b.rotate()
		elif operation == "rra":
			self.stack_a.reverse_rotate()
		elif operation == "rrb":
			self.stack_b.reverse_rotate()
		elif operation == "rrr":
			self.stack_a.reverse_rotate()
			self.stack_b.reverse_rotate()

	def visualize_operations(self):
		if self.operation_index >= len(self.operations) or not self.is_playing:
			self.is_playing = False
			return
		self.execute_operation(self.operations[self.operation_index])
		self.draw_stacks()
		self.select_operation(self.operation_index)
		self.operation_index += 1

		delay = int(1000 / self.speed_scale.get())
		self.root.after(delay, self.visualize_operations)

	def play_visualization(self):
		self.is_playing = not self.is_playing
		if self.is_playing:
			self.visualize_operations()

	def step_forward(self):
		self.is_playing = False
		if self.operation_index >= len(self.operations):
			return
		self.execute_operation(self.operations[self.operation_index])
		self.draw_stacks()
		self.select_operation(self.operation_index)
		self.operation_index += 1

	def step_backward(self):
		self.is_playing = False
		if self.operation_index <= 0:
			return
		self.operation_index -= 1
		self.execute_operation(reverse_operation(self.operations[self.operation_index]))
		self.draw_stacks()
		self.select_operation(self.operation_index)

	def select_operation(self, index):
		self.operations_list.selection_clear(0, tk.END)
		self.operations_list.selection_set(index)
		self.operations_list.activate(index)

	def generate_random_stack(self):
		try:
			num_elements = int(self.count_entry.get())
			if num_elements <= 0:
				raise ValueError("Number of elements must be positive.")
			self.values = random.sample(range(1, num_elements + 1), num_elements)
			self.input_entry.delete(0, tk.END)
			self.input_entry.insert(tk.END, " ".join(map(str, self.values)))
			self.draw_stacks()
		except ValueError:
			self.count_entry.delete(0, tk.END)
			self.count_entry.insert(0, "10")

	def run_push_swap(self):
		self.is_playing = False
		try:
			input_values = self.input_entry.get()
			result = subprocess.run([args.path] + input_values.split(), text=True, capture_output=True, timeout=5, check=True)
			self.operations = result.stdout.strip().split("\n")
			self.operation_index = 0

			self.operations_list.delete(0, tk.END)
			for operation in self.operations:
				self.operations_list.insert(tk.END, operation)
			self.values = list(map(int, input_values.split()))
			self.stack_a.elements = self.values.copy()
			self.stack_b.clear()
			self.calculate_bar_config()
			self.draw_stacks()
		except FileNotFoundError:
			print("Error: push_swap executable not found.")
		except subprocess.TimeoutExpired:
			print("Error: push_swap took too long to execute.")
		except subprocess.CalledProcessError as e:
			print(f"Error: push_swap failed:\n{e.stderr}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Visualizer for Push Swap project")
	parser.add_argument("--path", type=str, default="./push_swap", help="push_swap executable path")
	args = parser.parse_args()
	root = tk.Tk()
	root.title("Push Swap Visualizer")

	visualizer = PushSwapVisualizer(root)

	visualizer.draw_stacks()
	root.mainloop()