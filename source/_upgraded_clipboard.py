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


import _records


class Service():
	def __init__(self, system_clipboard):
		self.__system_clipboard = system_clipboard
		self.__records = _records.Stack()

		self.__temporary_record = None
		self.__skip_message = False

	def update(self):
		if self.__system_clipboard.has_data_been_updated():
			if self.__skip_message:
				self.__skip_message = False
				return

			if self.__temporary_record:
				self.__records.push(self.__temporary_record)
			self.__temporary_record = self.__system_clipboard.get_data()

	def clear_buffer(self):
		self.__records.clear()

	def paste(self):
		self.__skip_message = True
		self.__temporary_record = None

		data_to_push = self.__records.pop()
		if not data_to_push:
			return

		self.__system_clipboard.push_data(data_to_push)
