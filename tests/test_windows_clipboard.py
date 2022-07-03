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
import ctypes
import time
from ctypes import wintypes
from source import _windows_clipboard


class WindowsClipboardTest(unittest.TestCase):
	def setUp(self):
		windll = ctypes.windll
		msvcrt = ctypes.CDLL('msvcrt')

		self.__command_open_clipboard = windll.user32.OpenClipboard
		self.__command_open_clipboard.argtypes = [wintypes.HWND]
		self.__command_open_clipboard.restype = wintypes.BOOL

		self.__command_close_clipboard = windll.user32.CloseClipboard
		self.__command_close_clipboard.argtypes = []
		self.__command_close_clipboard.restype = wintypes.BOOL

		self.__command_get_clipboard_data = windll.user32.GetClipboardData
		self.__command_get_clipboard_data.argtypes = [wintypes.UINT]
		self.__command_get_clipboard_data.restype = wintypes.HANDLE

		self.__command_global_alloc = windll.kernel32.GlobalAlloc
		self.__command_global_alloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
		self.__command_global_alloc.restype = wintypes.HGLOBAL

		self.__command_global_lock = windll.kernel32.GlobalLock
		self.__command_global_lock.argtypes = [wintypes.HGLOBAL]
		self.__command_global_lock.restype = wintypes.LPVOID

		self.__command_global_unlock = windll.kernel32.GlobalUnlock
		self.__command_global_unlock.argtypes = [wintypes.HGLOBAL]
		self.__command_global_unlock.restype = wintypes.BOOL

		self.__command_wcslen = msvcrt.wcslen
		self.__command_wcslen.argtypes = [ctypes.c_wchar_p]
		self.__command_wcslen.restype = wintypes.UINT


		self.__GLOBAL_ALLOC_ATTRIBUTE_GMEM_MOVEABLE = 0x0002
		self.__CF_TEXT_CODE = 13

		self.__template = _windows_clipboard.Service(0.5)

	def __push_test_text(self, text):
		test_data = {}
		test_text_size = (self.__command_wcslen(text) + 1) * ctypes.sizeof(ctypes.c_wchar)

		handle = self.__command_global_alloc(self.__GLOBAL_ALLOC_ATTRIBUTE_GMEM_MOVEABLE, test_text_size)
		locked_handle = self.__command_global_lock(handle)

		ctypes.memmove(ctypes.c_wchar_p(locked_handle), ctypes.c_wchar_p(text), test_text_size)
		test_data[self.__CF_TEXT_CODE] = handle

		self.__template.push_data(test_data)

	def __get_test_text(self):
		if not self.__command_open_clipboard(None):
			return
		handle = self.__command_get_clipboard_data(self.__CF_TEXT_CODE)

		locked_handle = self.__command_global_lock(handle)
		result = str(ctypes.c_wchar_p(locked_handle).value)

		self.__command_global_unlock(handle)
		self.__command_close_clipboard()

		return result

	def test_push_data(self):
		test_text = "push_test"
		self.__push_test_text(test_text)

		self.assertEqual(test_text, self.__get_test_text())


	def test_ping_pong(self):
		first_state = "first_state"
		self.__push_test_text(first_state)

		saved_first_state = self.__template.get_data()

		second_state = "second_state"
		self.__push_test_text(second_state)

		self.__template.push_data(saved_first_state)

		self.assertEqual(first_state, self.__get_test_text())

	def test_has_data_been_updated(self):
		success = False

		self.__template.add_listener()
		self.__push_test_text("has_data_been_updated_test")

		time_for_test = time.time() + 0.5
		while time.time() < time_for_test:
			success = self.__template.has_data_been_updated()

			if success:
				self.assertTrue(success)
				return