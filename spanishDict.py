# coding=utf-8

import io 								#for file read / write
from time import strftime, localtime	#for filenaming with timestamp
import urllib, urllib2					#for the program to visit dictionary website
from pyquery import PyQuery as pq 		#pyQuery, like jQuery, search HTML node tree

class SpanishDictParser:
	baseURL = "http://www.spanishdict.com/translate/"
	encoding = "utf-8"
	readfile = "spanishDict.txt"
	list_of_fields = ["word", "brief definition", "part of speech", "example - spanish", "example - english"]

	file_name_base = "anki_import_"
	file_extension = ".txt"

	def __init__(self, readfile = None, baseURL = None, list_of_fields = None, file_name_base = None, file_extension = None):
		if readfile is not None:
			self.readfile = readfile

		if baseURL is not None:
			self.baseURL = baseURL

		if list_of_fields is not None:
			self.list_of_fields = list_of_fields

		if file_name_base is not None:
			self.file_name_base = file_name_base

		if file_extension is not None:
			self.file_extension = file_extension

		vocab_list = self.readFile()
		result = []
		for word in vocab_list:
			print "Searching on SpanishDict for " + word + "."
			dictPage = self.lookupSpanishDict(word)
			dictFields = self.getDictFields(dictPage)
			dictFieldList = self.fieldsToList(dictFields)
			dictLine = self.listToLine(dictFieldList)

			result.append(dictLine)

		resultContent = "\n".join(result)
		self.writeFile(self.generateFileName(), resultContent)

	def writeFile(self, filePath, content, encode = True):
		file = io.open(filePath, "w+", encoding=self.encoding)

		if encode == True:
			file.write(unicode(content, self.encoding))
		else:
			file.write(content)
		file.close()

	# Read the file that contains a vocab list that you need to look up.
	def readFile(self, filePath = None):
		if filePath is None:
			filePath = self.readfile

		file = io.open(filePath, "r", encoding="utf-8-sig")

		if file.mode == "r":
			content = file.readlines()

			# originally a <unicode> object list,
			# If we add encode() to x, will make it a string list
			content = [x.strip().encode(self.encoding) for x in content]
		file.close()
		return content

	# Generate a file with the word"s definition and possibly an example, which Anki can import
	# The file name is generated with timestamp so that it never overwrite previous ones.
	def generateFileName(self):
		time = strftime("%Y%m%d%H%M%S", localtime())
		return self.file_name_base + time + self.file_extension

	# According to the word, get back the relavant dictionary page"s HTML code.
	# The word should be a UTF-8 encoded string
	def lookupSpanishDict(self, word):
		quotedWord = urllib.quote(word)
		URL = self.baseURL + quotedWord

		response = urllib2.urlopen(URL)

		html = response.read().decode(self.encoding)
		return html

	# Generates a dict item that includes dictionary fields
	def getDictFields(self, page):
		tab = pq(page)(".tab-content")

		if len(tab) == 0:
			d = pq(page)(".translate .card")
		else:
			d = pq(page)(".tab-pane.active")

		word = d(".source-text").text().encode("utf-8") 	# Get the word itself from the dictionary page
		brief_definition = d(".lang .el").text().encode("utf-8")	# Get the word"s brief definition

		dictionary = d(".dictionary-neodict") # For more details, search NeoDict only
		part_of_speech = dictionary(".part_of_speech:first").text().encode("utf-8") # Get the word"s part of speech
		example = {
			"es": dictionary(".dictionary-neodict-example:first > span:first").text().encode("utf-8"),
			"en": dictionary(".dictionary-neodict-example:first > em").text().encode("utf-8")
		}

		return {
			self.list_of_fields[0]: word,
			self.list_of_fields[1]: brief_definition,
			self.list_of_fields[2]: part_of_speech,
			self.list_of_fields[3]: example["es"],
			self.list_of_fields[4]: example["en"]
		}

	# turn a dict item into a list
	def fieldsToList(self, fields, list_of_fields = None):
		if list_of_fields is None:
			list_of_fields = self.list_of_fields
		temp_list = []
		for field in list_of_fields:
			temp_list.append(fields[field])
		return temp_list

	# given a list of dictionary fields,
	# return a text line that contains all the fields
	def listToLine(self, list, separator = "\t"):
		return separator.join(list)

if __name__ == "__main__":
	spanishDictParser = SpanishDictParser()

