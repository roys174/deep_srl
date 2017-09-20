#!/usr/bin/python 

import sys
import re
import glob
from string import maketrans
from FileTools import *

_end = '_end_'

def main(args):
	argc = len(args)

	if argc < 2:
		print "Usage:",args[0],"<xml dir> <of>"
		return -1

	ifiles = glob.glob(args[1]+'/*_full.xml')

	with openWriteFile(args[2]) as ofh:
		for ifile in ifiles:
			print ifile
			process_file(ifile, ofh)

	return 0

def process_file(ifile, ofh):
	v = ifile.split("/")[-1].split('_')[0]

	i = 0
	with openReadFile(ifile) as ifh:
		text = v_index = bios = args = in_arg = None
		j = -1
		
		for l in ifh:
			l = re.sub("^[ \t]+", "", l.rstrip())
			
			if len(l) == 0:
				continue

			print l
			if text is None:
				if l == '<text>':
					#print "TEXT!!!"
					i += 1
					text = []
					args = []
					bios = []
					bad = 0
			elif j < 0:
				if l[:8] == '<arg n="' and l[8].isdigit():
					l = l.translate(maketrans("",""), '[]')
					l = re.sub("\(", "( ", l)
					l = re.sub("\)", " )", l)
					l = re.sub("\b\?", " ?", l)
					e = l.split(">")[1]

					if e != '-':
						e2 = e.split()
						args.append(e2)
						args[-1].append(l[8])
						print("New arg", l[8], e2)

				elif l  == '<fdg>':
					args = make_trie(args)
					j = 0
			elif l == '</fdg>':
				if bad == 0:
					if v_index is None:
						print "### Can't find verb",v,"for ",text,"in",ifile
					else:
						if len(text) != len(bios):
							print "Problem:",len(text),"!=",len(bios)
							sys.exit(-1)
						ofh.write(str(v_index)+" "+" ".join(text)+" ||| "+" ".join(bios)+"\n")
				
				text = v_index = bios = in_arg = None
				j = -1
				bad = 0
			elif bad == 1:
				continue
			else:
				l = re.sub("^<line>[ \t]*", "", l)
				if not re.match("^[0-9]+\t", l):
					continue
				else:
					j = int(l.split("\t")[0]) - 1

				e = re.split("	| {4,}", l)

				text.append(re.sub(" ", "-", e[1]))
				# print "Adding",e[1]
				if len(e) > 2:
					# If inside arg
					if in_arg is not None:
						#print "Here!"
						# Mistake - not really arg
						if e[1] not in in_arg:
							# End of argument
							if _end in in_arg:
								#print "ending with",in_arg[_end]
								for m in range(in_arg_count):
									bios[len(bios)-m-1] += str(in_arg[_end])
							# False alarm
							else:	
								#print "mistake?"
							
								# Undo all changes
								for m in range(in_arg_count):
									bios[len(bios)-m-1] = "O"
	
							in_arg = None
							in_arg_count = 0
						# Another word in the arugment
						else:
							bios.append("I-A")
							# print "Adding I-A"

							in_arg = in_arg[e[1]]
							#print "GReat!",type(in_arg),in_arg
							in_arg_count += 1
						
							# End of argument	
							continue
					# If this is the main verb
					if e[2] == v:
						# Already saw this verb, can't decide which is the correct one
						if v_index is not None:
							print "### Text",text,"has two occorrences of",v
							bad = 1
							continue
						else:
							v_index = j
							bios.append("B-V")
							# print "Adding B-V"
					# New argument!
					elif e[1] in args:
						in_arg = args[e[1]]
						bios.append("B-A")
						# print "Adding B-A"
						in_arg_count = 1
					else:
						bios.append("O")
						# print "Adding O"
				else:
					bios.append("O")
					# print "Adding 2 O"


def make_trie(arr):
	root = dict()
	for k in arr:
	    current_dict = root
	    for w in k[:-1]:
	        current_dict = current_dict.setdefault(w, {})
	    current_dict[_end] = k[-1]
	return root
	
					
				
				
if __name__ == "__main__":
	sys.exit(main(sys.argv))
