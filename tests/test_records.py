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


import unittest
import random
from source import _records


class RecordsTest(unittest.TestCase):
	def setUp(self):
		self.__template = _records.Stack()

	def test_push(self):
		class random_object(object):
			pass

		self.__template.push(random_object)
		self.assertEqual(1, self.__template.get_size())

	def test_peek(self):
		self.__template = _records.Stack()

		self.assertEqual(None, self.__template.peek())

		for index in range(10):
			random_integer = random.randrange(100)
			self.__template.push(random_integer)

			self.assertEqual(random_integer, self.__template.peek())
			self.assertEqual(index + 1, self.__template.get_size())

	def test_pop(self):
		self.__template = _records.Stack()

		self.assertEqual(None, self.__template.pop())

		for index in range(10):
			random_integer = random.randrange(100)
			self.__template.push(random_integer)

			self.assertEqual(random_integer, self.__template.pop())
			self.assertEqual(0, self.__template.get_size())

	def test_contains(self):
		self.__template = _records.Stack()
		random_integer = random.randrange(300)

		self.assertEqual(False, self.__template.contains(random_integer))
		
		self.__template.push(random_integer)
		self.assertEqual(True, self.__template.contains(random_integer))
		self.assertEqual(False, self.__template.contains(random_integer - 1))

	def test_clear_stack(self):
		class random_object(object):
			pass

		self.__template = _records.Stack()

		self.__template.push(random_object)
		self.__template.clear()

		self.assertEqual(0, self.__template.get_size())