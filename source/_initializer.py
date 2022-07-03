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


from sys import platform
import keyboard
import time
import _windows_clipboard
import _upgraded_clipboard


class Instruments():
	def __setup_os_clipboard(self):
		self.__os_clipboard = None

		if platform == "win32":
			self.__os_clipboard = _windows_clipboard.Service(0.5)

			if not self.__os_clipboard.add_listener():
				return False

		if self.__os_clipboard:
			return True
		return False

	def setup_clever_clipboard(self):
		if not self.__setup_os_clipboard():
			return None

		return _upgraded_clipboard.Service(self.__os_clipboard)

class HotKeys():
	def __init__(self):
		print("________________________Info________________________")

	def setup_clear_buffer(self, logic):
		hotkeys = "Alt + Delete"
		print("Command clear buffer attach to " + hotkeys)

		keyboard.add_hotkey(hotkeys, logic)

	def setup_clever_paste(self, logic):
		hotkeys = "Alt + V"
		print("Command move down along the buffer attach to " + hotkeys)

		keyboard.add_hotkey(hotkeys, logic)


