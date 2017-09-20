#!/usr/bin/python 

from __future__ import print_function

import sys
import re
import glob
import nltk
from nltk.stem import WordNetLemmatizer
from string import maketrans

from FileTools import *

reload(sys)
sys.setdefaultencoding('utf8')

_end = '_end_'

def main(args):
	argc = len(args)

	if argc < 2:
		print ("Usage:",args[0],"<xml dir> <of>")
		return -1

	ifiles = glob.glob(args[1]+'/*_full.xml')

	wordnet_lemmatizer = WordNetLemmatizer()

	with openWriteFile(args[2]) as ofh:
		for ifile in ifiles:
			print (ifile)
			process_file(ifile, ofh, wordnet_lemmatizer)

	return 0

def process_file(ifile, ofh, wordnet_lemmatizer):
	v = ifile.split("/")[-1].split('_')[0]

	i = 0

	with openReadFile(ifile) as ifh:
		text = v_index = bios = args = in_arg = None
		j = -1

		l = ifh.readline()

		while l:
			l = re.sub("^[ \t]+", "", l.rstrip())
			
			if len(l) == 0:
				l = ifh.readline()
				continue

			# print (l)
			if text is None:
				if l == '<text>':
					i += 1
					l = ifh.readline().rstrip().lower().replace("&apos;", "'")
					text = nltk.tokenize.word_tokenize(l)
					args = []
					all_args = []
					bad = 0
			elif l[:8] == '<arg n="' and l[8].isdigit():
					l = l.translate(maketrans("",""), '[]').lower()
					l = l.replace("&apos;", "'")
					# l = re.sub("\(", "( ", l)
					# l = re.sub("\)", " )", l)
					# l = re.sub("\b\?", " ?", l)
					e = re.split("[<>]", l)[2]

					if e != '-':
						e2 = nltk.tokenize.word_tokenize(e)
						# print("Adding",e2,"with",l[8])
						args.append(e2)
						args[-1].append(l[8])
						all_args.append(l[8])
						# print("New arg", l[8], e2)

			elif l  == '<fdg>':
					args_trie = make_trie(args)

					v_index = None
					for i in range(len(text)):
						w = unicode(text[i], errors='ignore')

						if w[-2:] == "_v":
							text[i] = w[:-2]
							v_index = i
						elif w[-2:] == "_n":
							text[i] = w[:-2]
							continue
						else:
							potential_v = wordnet_lemmatizer.lemmatize(w, pos='v')

							# print(potential_v)

							if potential_v == v:
								if v_index is None:
									v_index = i
								else:
									print("### Text", " ".join(text), "has at least two occorrences of", v)
									v_index = None
									break

					if v_index is None:
						print("#### Can't find verb", v, "for", " ".join(text), "in", ifile)
					else:
						gen_output(text, args_trie, all_args, v_index, ofh)

					text = None

					j = 0
			# elif l == '</fdg>':
            #
			# 	if bad == 0:
			# 		if v_index is None:
			# 			print ("### Can't find verb",v,"for ",text,"in",ifile)
			# 		else:
			# 			gen_output(text, args_trie, all_args, v_index, ofh)
            #
			# 			text = None
			# 		# if len(text) != len(bios):
			# 			# 	print "Problem:",len(text),"!=",len(bios)
			# 			# 	sys.exit(-1)
			# 			# ofh.write(str(v_index)+" "+" ".join(text)+" ||| "+" ".join(bios)+"\n")
			#
			# 	text = v_index = bios = in_arg = None
			# 	j = -1
			# 	bad = 0
			# elif bad == 1:
			# 	l = ifh.readline()
			# 	continue
			# else:
			# 	l = re.sub("^<line>[ \t]*", "", l)
			# 	if not re.match("^[0-9]+\t", l):
			# 		l = ifh.readline()
			# 		continue
			# 	else:
			# 		j = int(l.split("\t")[0]) - 1
            #
			# 	e = re.split("	| {4,}", l)
            #
			# 	# text.append(re.sub(" ", "-", e[1]))
			# 	# print "Adding",e[1]
			# 	if len(e) > 2:
			# 		# If inside arg
			# 		# if in_arg is not None:
			# 		# 	#print "Here!"
			# 		# 	# Mistake - not really arg
			# 		# 	if e[1] not in in_arg:
			# 		# 		# End of argument
			# 		# 		if _end in in_arg:
			# 		# 			#print "ending with",in_arg[_end]
			# 		# 			for m in range(in_arg_count):
			# 		# 				bios[len(bios)-m-1] += str(in_arg[_end])
			# 		# 		# False alarm
			# 		# 		else:
			# 		# 			#print "mistake?"
			# 		#
			# 		# 			# Undo all changes
			# 		# 			for m in range(in_arg_count):
			# 		# 				bios[len(bios)-m-1] = "O"
             #        #
			# 		# 		in_arg = None
			# 		# 		in_arg_count = 0
			# 		# 	# Another word in the arugment
			# 		# 	else:
			# 		# 		bios.append("I-A")
			# 		# 		# print "Adding I-A"
             #        #
			# 		# 		in_arg = in_arg[e[1]]
			# 		# 		#print "GReat!",type(in_arg),in_arg
			# 		# 		in_arg_count += 1
			# 		#
			# 		# 		# End of argument
			# 		# 		continue
			# 		# # If this is the main verb
			# 		if e[2] == v:
			# 			# Already saw this verb, can't decide which is the correct one
			# 			if v_index is not None:
			# 				print ("### Text",text,"has two occorrences of",v)
			# 				bad = 1
			# 				l = ifh.readline()
			# 				continue
			# 			else:
			# 				v_index = j
			# 				# bios.append("B-V")
			# 				# print "Adding B-V"
			# 		# New argument!
			# 		# elif e[1] in args:
			# 		# 	in_arg = args[e[1]]
			# 		# 	bios.append("B-A")
			# 		# 	# print "Adding B-A"
			# 		# 	in_arg_count = 1
			# 		# else:
			# 		# 	bios.append("O")
			# 		# 	# print "Adding O"
			# 	# else:
			# 	# 	bios.append("O")
			# 	# 	# print "Adding 2 O"
			l = ifh.readline()


def make_trie(arr):
	root = dict()
	for k in arr:
	    current_dict = root
	    for w in k[:-1]:
	        current_dict = current_dict.setdefault(w, {})
	    current_dict[_end] = k[-1]
	return root
	
					

def gen_output(text, args_trie, all_args, v_index, ofh):
	written = []
	next_i = 0
	ofh.write(str(v_index)+" "+" ".join(text)+" |||")
	while next_i < len(text):
		# print("ni is",next_i, text[next_i])
		if next_i == v_index:
			ofh.write(" B-V")
			next_i += 1
		else:
			arg, next_i = write_arg(text, next_i, args_trie, ofh)

			if arg is not None:
				written.append(arg)

	if len(all_args) > len(written):
		print("@@@: "+" ".join(text),": only",len(written),"args written, expected",len(all_args))

	ofh.write("\n")

def write_arg(text, next_i, args_trie, ofh):
	tmp_i = next_i
	value = None

	tmp_trie = args_trie
	# print("Test",text[tmp_i])
	while tmp_i < len(text) and text[tmp_i] in tmp_trie:
		# print("In! Test", text[tmp_i])
		tmp_trie = tmp_trie[text[tmp_i]]
		tmp_i += 1

	if _end in tmp_trie:
		# print("Galula!")
		value = tmp_trie[_end]

		ofh.write(" B-A"+str(value))

		next_i += 1

		while next_i < tmp_i:
			next_i += 1
			ofh.write(" I-A"+str(value))
	else:
		# print("no galula?:*(")
		ofh.write(" O")
		next_i += 1

	return value, next_i



				
if __name__ == "__main__":
	sys.exit(main(sys.argv))
