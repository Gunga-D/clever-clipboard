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
import test
import random
from source import _upgraded_clipboard
import dummy_clipboard


class UpgradedClipboardTest(unittest.TestCase):
	def setUp(self):
		self.__clipboard = dummy_clipboard.Service()
		self.__upgraded_clipboard = _upgraded_clipboard.Service(self.__clipboard)

	def __fill_upgraded_clipboard(self, tests_number):
		filling_data = []

		for index in range(tests_number):
			number = random.randrange(1, 100)

			filling_data.append(number)
			self.__clipboard.push_data(number)

			self.__upgraded_clipboard.update()

		return filling_data

	def test_transfer_data(self):
		tests_number = 10
		test_data = self.__fill_upgraded_clipboard(tests_number)

		for test_index in reversed(range(tests_number)):
			self.assertEqual(test_data[test_index], self.__clipboard.get_data())
			self.__upgraded_clipboard.paste()

	def test_clear_buffer(self):
		self.__fill_upgraded_clipboard(10)

		self.__upgraded_clipboard.clear_buffer()
		self.assertEqual(None, self.__upgraded_clipboard.paste())