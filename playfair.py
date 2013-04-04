#!/usr/bin/python3
#  playfair.py
#  
#  Copyright 2013 Robert Knauer <robert@privatdemail.net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import math

class Playfair (object):
	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	
	def __init__ (self):
		pass
	def __del__ (self):
		pass
	def prepare_text (self, text):
		## Remove umlauts:
		text_p = text.replace("ß", "ss").replace("ẞ", "SS")
		text_p = text_p.replace("ü", "ue").replace("Ü", "UE")
		text_p = text_p.replace("ö", "oe").replace("Ö", "OE")
		text_p = text_p.replace("ä", "ae").replace("Ä", "AE")
		## Remove spaces and punctuation:
		text_p = text_p.replace(" ", "")
		text_p = text_p.replace(".", "")
		text_p = text_p.replace("!", "")
		text_p = text_p.replace("?", "")
		## Make all letters upper case:
		text_p = text_p.upper()
		## Replace J with I:
		text_p = text_p.replace("J", "I")
		## Seperate into pairs and seperate double letters with an X:
		lastc = ""
		text_s = []
		for c in list(text_p):
			if lastc == "":
				lastc = c
			elif lastc == c and c != "X":
				text_s.append((lastc, "X"))
				lastc = c
			else:
				text_s.append((lastc, c))
				lastc = ""
		## Append an X to the last letter if necessary:
		if lastc != "":
			text_s.append((lastc, "X"))
		return text_s
	def concat_seperated_text (self, text_s):
		text = ""
		for pair in text_s:
			text += "%s%s " % (pair[0], pair[1], )
		return text.strip()
	def create_square (self, key):
		square = []
		alph_remain = self.alphabet[:]
		for i in range(25):
			if len(key) > i:
				square.append(key[i])
				alph_remain.remove(key[i])
			else:
				square.append(alph_remain[0])
				alph_remain.pop(0)
		return square
	def dump_square (self, square):
		for i in range(25):
			if i is not 0 and i % 5 is 0:
				print("")
			print(square[i], end=" ")
		print("")
	def get_square_row (self, i):
		return math.floor(i/5.)
	def get_square_col (self, i):
		return i-(self.get_square_row(i)*5)
	def get_square_below (self, square, i):
		row = self.get_square_row(i)
		col = self.get_square_col(i)
		if row == 4:
			row = 0
		else:
			row += 1
		return square[(row*5)+col]
	def get_square_rightof (self, square, i):
		row = self.get_square_row(i)
		col = self.get_square_col(i)
		if col == 4:
			col = 0
		else:
			col += 1
		return square[(row*5)+col]
	def get_square_above (self, square, i):
		row = self.get_square_row(i)
		col = self.get_square_col(i)
		if row == 0:
			row = 4
		else:
			row -= 1
		return square[(row*5)+col]
	def get_square_leftof (self, square, i):
		row = self.get_square_row(i)
		col = self.get_square_col(i)
		if col == 0:
			col = 4
		else:
			col -= 1
		return square[(row*5)+col]
	def check_key (self, key, debug):
		if debug:
			print("==> Checking key... ", end="")
		if len(key) < 1 or len(key) > 25:
			if debug:
				print("Fail.")
				print("====> Invalid key size: %d" % len(key))
			return False
		alph_remain = self.alphabet[:]
		for c in list(key):
			if not c in self.alphabet:
				if debug:
					print("Fail.")
					print("====> Invalid char in the key: %s" % c)
				return False
			elif not c in alph_remain:
				if debug:
					print("Fail.")
					print("====> Double char in the key: %s" % c)
				return False
			else:
				alph_remain.remove(c)
		if debug:
			print("Done.")
		return True
	def encode (self, text, key, debug=False):
		if debug:
			print("== PLAYFAIR encode start ==")
		## Prepare the text:
		if debug:
			print("==> Preparing...")
			print("Text: %s" % text)
		text_s = self.prepare_text(text)
		if debug:
			print("Prepared Text: %s" % self.concat_seperated_text(text_s))
			print("Key: %s" % key)
		## Check the key:
		if not self.check_key(key, debug):
			return False
		## Create the square:
		if debug:
			print("==> Creating playfair square...")
		square = self.create_square(key)
		if debug:
			self.dump_square(square)
		## Encode:
		if debug:
			print("==> Encoding...")
		text_e = ""
		for pair in text_s:
			i0 = square.index(pair[0])
			i1 = square.index(pair[1])
			if self.get_square_col(i0) == self.get_square_col(i1):
				# same column
				text_e += self.get_square_below(square, i0)
				text_e += self.get_square_below(square, i1)
			elif self.get_square_row(i0) == self.get_square_row(i1):
				# same row
				text_e += self.get_square_rightof(square, i0)
				text_e += self.get_square_rightof(square, i1)
			else:
				# neither same column nor same row
				text_e += square[(self.get_square_row(i0)*5)+self.get_square_col(i1)]
				text_e += square[(self.get_square_row(i1)*5)+self.get_square_col(i0)]
		## Split into pairs:
		text = ""
		for i in range(0, len(text_e), 2):
			text += "%s " % text_e[i:(i+2)]
		text = text.strip()
		if debug:
			print("Encoded Text: %s" % text)
		## Success:
		if debug:
			print("== PLAYFAIR encode done ==")
		return text
	def decode (self, text, key, debug=False):
		if debug:
			print("== PLAYFAIR decode start ==")
		## Print the arguments:
		if debug:
			print("====> Preparing...")
		if debug:
			print("Encoded text: %s" % text)
		if debug:
			print("Key: %s" % key)
		## Check the key:
		if not self.check_key(key, debug):
			return False
		## Create the square:
		if debug:
			print("==> Creating playfair square...")
		square = self.create_square(key)
		if debug:
			self.dump_square(square)
		## Decode:
		if debug:
			print("==> Decoding...")
		text_e = text.split(" ")
		text_d = ""
		for pair in text_e:
			i0 = square.index(pair[0])
			i1 = square.index(pair[1])
			if self.get_square_col(i0) == self.get_square_col(i1):
				# same column
				text_d += self.get_square_above(square, i0)
				text_d += self.get_square_above(square, i1)
			elif self.get_square_row(i0) == self.get_square_row(i1):
				# same row
				text_d += self.get_square_leftof(square, i0)
				text_d += self.get_square_leftof(square, i1)
			else:
				# neither same column nor same row
				text_d += square[(self.get_square_row(i0)*5)+self.get_square_col(i1)]
				text_d += square[(self.get_square_row(i1)*5)+self.get_square_col(i0)]
		## Split into pairs:
		text = ""
		for i in range(0, len(text_d), 2):
			text += "%s " % text_d[i:(i+2)]
		text = text.strip()
		if debug:
			print("Decoded Text: %s" % text)
		## Success:
		if debug:
			print("== PLAYFAIR decode done ==")
		return text

if __name__ == "__main__":
	p = Playfair()
	txt = "Laboulaye lady will lead to Cibola temples of gold."
	key = "DEATH"
	print("Text: %s" % txt)
	print("Key: %s" % key)
	enc = p.encode(txt, key, False) # True to enable debug mode
	print("Encrypted: %s" % enc)
	dec = p.decode(enc, key, False) # True to enable debug mode
	print("Decrypted: %s" % dec)
