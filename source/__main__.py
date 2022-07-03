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


import _initializer


if __name__ == "__main__":
	instruments = _initializer.Instruments()
	upgraded_clipboard = instruments.setup_clever_clipboard()
	if not upgraded_clipboard:
		print("Error: clipboard setup error...")

	hotkeys = _initializer.HotKeys()
	hotkeys.setup_clear_buffer(upgraded_clipboard.clear_buffer)
	hotkeys.setup_clever_paste(upgraded_clipboard.paste)

	print("\nUpgraded clipboard launсhed...")
	while True:
		upgraded_clipboard.update()
