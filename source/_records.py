#clever-clipboard
#Copyright (c) 2022 Gunga Dondokov
 
#Permission is hereby granted, free of charge, to any person obtaining
#a copy of this software and associated documentation files (the
#"Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
 
#The above copyright notice and this permission notice shall be included
#in all copies or substantial portions of the Software.
 
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


class Stack():
	def __init__(self):
		self.__stack = []

	def clear(self):
		self.__stack.clear()

	def contains(self, element):
		return element in self.__stack

	def push(self, element):
		self.__stack.append(element)

	def pop(self):
		if len(self.__stack) <= 0:
			return None

		return self.__stack.pop()

	def peek(self):
		if len(self.__stack) <= 0:
			return None
			
		last_element_index = len(self.__stack) - 1
		return self.__stack[last_element_index]

	def get_size(self):
		return len(self.__stack)