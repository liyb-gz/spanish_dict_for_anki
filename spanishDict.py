# coding=utf-8

import os #for file read / write
from time import strftime, localtime #for filenaming with timestamp

def writeFile(filePath, content):
	file = open(filePath, "w+")
	file.write(content)
	file.close()

text = 'alojar\tto accommodate\tPodremos alojar 3,000 huéspedes en nuestro hotel.'

def generateFileName():
	file_name_base = "anki_import_"
	file_extension = ".txt"
	time = strftime("%Y%m%d%H%M%S", localtime())
	return file_name_base + time + file_extension

writeFile(generateFileName(), text)