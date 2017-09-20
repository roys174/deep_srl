#############################################################
#															#
#	This file contains tools for openning files 			#
#	with various types of encoding for reading/writing.		#
#	Author: Roy Schwartz (roys02@cs.huji.ac.il)				#
#															#
#############################################################

#!/usr/local/bin/python
import zipfile
import bz2
import gzip


def readZipFile(name, filename = None):
	z = zipfile.ZipFile(name, 'r')
	
	if (filename == None):
		filename = z.namelist()[0]
			
	try:
        	data = z.read(filename)
        	z.close()
	except KeyError:
        	print ('ERROR: Did not find %s in zip file' % filename)
	else:
		return data.split("\n")

def openWriteGZipFile(name):
	return gzip.open(name, 'wt')

def openReadGZipFile(name):
	return gzip.open(name, 'rt')

def openWriteZipFile(name):
	return zipfile.ZipFile(name, 'w')

def readBZ2File(name):
	bz_file = bz2.BZ2File(name)
	return bz_file.readlines() 

def openWriteBZ2File(name):
	return bz2.BZ2File(name, 'w')
	
def openReadZipFile(name):
	return zipfile.ZipFile(name, 'r')

def openReadBZ2File(name):
	return bz2.open(name, 'r')


def readFile(name):
	if (name.endswith(".zip")):
		return readZipFile(name)
	elif (name.endswith('.bz2')):
		return readBZ2File(name)
	else:
		return readTextFile(name)

def readTextFile(name):
	f = open(name, "r")
	lines = f.readlines()
	f.close()
	
	return lines

def openWriteTextFile(name):
	return open(name, "w")

def openReadTextFile(name):
	return open(name, "r")



def openWriteFile(name):
	if (name.endswith(".zip")):
		return openWriteZipFile(name)
	elif (name.endswith('.bz2')):
		return openWriteBZ2File(name)
	elif (name.endswith('.gz')):
		return openWriteGZipFile(name)
	else:
		return openWriteTextFile(name)

def openReadFile(name):
	if (name.endswith(".zip")):
		return openReadZipFile(name)
	elif (name.endswith('.bz2')):
		return openReadBZ2File(name)
	elif (name.endswith('.gz')):
		return openReadGZipFile(name)
	else:
		return openReadTextFile(name)

