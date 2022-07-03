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


import ctypes
from ctypes import wintypes
import time
import _os_clipboard


class Service(_os_clipboard.IClipboardService):
	def __init__(self, waiting_time_to_clipboard):
		core = ctypes.windll

		self.__command_create_window = core.user32.CreateWindowExA
		self.__command_create_window.argtypes = [wintypes.DWORD, wintypes.LPCSTR, wintypes.LPCSTR, wintypes.DWORD, wintypes.INT, wintypes.INT,
												wintypes.INT, wintypes.INT, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID]
		self.__command_create_window.restype = wintypes.HWND

		self.__command_destroy_window = core.user32.DestroyWindow
		self.__command_destroy_window.argtypes = [wintypes.HWND]
		self.__command_destroy_window.restype = wintypes.BOOL

		self.__command_open_clipboard = core.user32.OpenClipboard
		self.__command_open_clipboard.argtypes = [wintypes.HWND]
		self.__command_open_clipboard.restype = wintypes.BOOL

		self.__command_close_clipboard = core.user32.CloseClipboard
		self.__command_close_clipboard.argtypes = []
		self.__command_close_clipboard.restype = wintypes.BOOL

		self.__command_count_clipboard_formats = core.user32.CountClipboardFormats
		self.__command_count_clipboard_formats.argtypes = []
		self.__command_count_clipboard_formats.restype = wintypes.UINT

		self.__command_enum_clipboard_formats = core.user32.EnumClipboardFormats
		self.__command_enum_clipboard_formats.argtypes = [wintypes.UINT]
		self.__command_enum_clipboard_formats.restype = wintypes.UINT

		self.__command_get_clipboard_data = core.user32.GetClipboardData
		self.__command_get_clipboard_data.argtypes = [wintypes.UINT]
		self.__command_get_clipboard_data.restype = wintypes.HANDLE

		self.__command_empty_clipboard = core.user32.EmptyClipboard
		self.__command_empty_clipboard.argtypes = []
		self.__command_empty_clipboard.restype = wintypes.BOOL

		self.__command_set_clipboard_data = core.user32.SetClipboardData
		self.__command_set_clipboard_data.argtypes = [wintypes.UINT, wintypes.HANDLE]
		self.__command_set_clipboard_data.restype = wintypes.HANDLE

		self.__command_add_clipboard_listener = core.user32.AddClipboardFormatListener
		self.__command_add_clipboard_listener.argtypes = [wintypes.HWND]
		self.__command_add_clipboard_listener.restype = wintypes.BOOL

		self.__command_remove_clipboard_listener = core.user32.RemoveClipboardFormatListener
		self.__command_remove_clipboard_listener.argtypes = [wintypes.HWND]
		self.__command_remove_clipboard_listener.restype = wintypes.BOOL

		self.__command_peek_message = core.user32.PeekMessageA
		self.__command_peek_message.argtypes = [wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT]
		self.__command_peek_message.restype = wintypes.BOOL

		self.__command_global_alloc = core.kernel32.GlobalAlloc
		self.__command_global_alloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
		self.__command_global_alloc.restype = wintypes.HGLOBAL

		self.__command_global_lock = core.kernel32.GlobalLock
		self.__command_global_lock.argtypes = [wintypes.HGLOBAL]
		self.__command_global_lock.restype = wintypes.LPVOID

		self.__command_global_unlock = core.kernel32.GlobalUnlock
		self.__command_global_unlock.argtypes = [wintypes.HGLOBAL]
		self.__command_global_unlock.restype = wintypes.BOOL

		self.__command_global_size = core.kernel32.GlobalSize
		self.__command_global_size.argtypes = [wintypes.HGLOBAL]
		self.__command_global_size.restype = ctypes.c_size_t


		self.__GLOBAL_ALLOC_ATTRIBUTE_GMEM_MOVEABLE = 0x0002
		self.__ENUM_CLIPBOARD_FORMATS_DEFAULT_PARAMETER = 0
		self.__PEEK_MESSAGE_ATTRIBUTE_PM_REMOVE = 0x0001
		self.__PEEK_MESSAGE_INDEX_OF_MESSAGE = 0x031D

		self.__window = self.__command_create_window(0, b"STATIC", None, 0, 0, 0, 0, 0, None, None, None, None)
		self.__was_listener_connected = False

		self.__waiting_time_to_clipboard = waiting_time_to_clipboard

	def __del__(self):
		if self.__was_listener_connected:
			self.remove_listener()
			
		self.__command_destroy_window(self.__window)

	def __security_open_clipboard(self):
		dropping_time = time.time() + self.__waiting_time_to_clipboard

		while time.time() < dropping_time:
			success = self.__command_open_clipboard(self.__window)

			if success:
				return True

		return False

	def add_listener(self):
		self.__was_listener_connected = True
		return self.__command_add_clipboard_listener(self.__window)
		
	def remove_listener(self):
		self.__was_listener_connected = False
		return self.__command_remove_clipboard_listener(self.__window)

	def has_data_been_updated(self):
		message = wintypes.MSG()
		is_message_available = self.__command_peek_message(ctypes.byref(message), self.__window,
			self.__PEEK_MESSAGE_INDEX_OF_MESSAGE, self.__PEEK_MESSAGE_INDEX_OF_MESSAGE, self.__PEEK_MESSAGE_ATTRIBUTE_PM_REMOVE)

		return is_message_available

	def push_data(self, data):
		if not self.__security_open_clipboard():
			return False

		self.__command_empty_clipboard()
		for format in data.keys():
			self.__command_global_unlock(data[format])

			handle = self.__command_set_clipboard_data(format, data[format])
			if not handle:
				return False

		self.__command_close_clipboard()

		return True

	def get_data(self):
		if not self.__security_open_clipboard():
			return None

		data = {}

		current_format = self.__command_enum_clipboard_formats(self.__ENUM_CLIPBOARD_FORMATS_DEFAULT_PARAMETER)
		for formatIndex in range(self.__command_count_clipboard_formats()):
			handle = self.__command_get_clipboard_data(current_format)
			if not handle:
				data[current_format] = None
				break
			locked_handle = self.__command_global_lock(handle)
			block_size = self.__command_global_size(handle)

			new_handle = self.__command_global_alloc(self.__GLOBAL_ALLOC_ATTRIBUTE_GMEM_MOVEABLE, block_size)
			new_locked_handle = self.__command_global_lock(new_handle)
			ctypes.memmove(ctypes.c_void_p(new_locked_handle), ctypes.c_void_p(locked_handle), block_size)
			data[current_format] = new_handle

			self.__command_global_unlock(handle)

			current_format = self.__command_enum_clipboard_formats(current_format)

		self.__command_close_clipboard()

		return data