#!/usr/bin/python
# FileName: Subsampling.py
# Version 1.0 by Tao Ban, 2010.5.26
# Modified by Curtis Miller, 2018.5.3
# This function extract all the contents, ie subject and first part from the .eml file
# and store it in a new file with the same name in the dst dir.

import email.parser
import os, sys, stat
import shutil

def ExtractSubPayload(filename):
	''' Extract the subject and payload from the .eml file.

	'''
	if not os.path.exists(filename): # dest path doesnot exist
		print("ERROR: input file does not exist:", filename)
		os.exit(1)
	fp = open(filename, encoding="latin1")
	msg = email.message_from_file(fp)
	payload = msg.get_payload()
	if type(payload) == type(list()) :
		payload = payload[0] # only use the first part of payload
	sub = msg.get('subject')
	sub = str(sub)
	if type(payload) != type('') :
		payload = str(payload)

	return sub + payload

def ExtractBodyFromDir(srcdir, dstdir):
	'''Extract the body information from all .eml files in the srcdir and

	save the file to the dstdir with the same name.'''
	if not os.path.exists(dstdir): # dest path doesnot exist
		os.makedirs(dstdir)
	files = os.listdir(srcdir)
	for file in files:
		srcpath = os.path.join(srcdir, file)
		dstpath = os.path.join(dstdir, file)
		src_info = os.stat(srcpath)
		if stat.S_ISDIR(src_info.st_mode): # for subfolders, recurse
			ExtractBodyFromDir(srcpath, dstpath)
		else:  # copy the file
			body = ExtractSubPayload (srcpath)
			dstfile = open(dstpath, 'w', encoding="latin1")
			dstfile.write(body)
			dstfile.close()


###################################################################
# main function start here
# srcdir is the directory where the .eml are stored
print('Input source directory: ') #ask for source and dest dirs
srcdir = input()
if not os.path.exists(srcdir):
	print('The source directory %s does not exist, exit...' % (srcdir))
	sys.exit()
# dstdir is the directory where the content .eml are stored
print('Input destination directory: ') #ask for source and dest dirs
dstdir = input()
if not os.path.exists(dstdir):
	print('The destination directory is newly created.')
	os.makedirs(dstdir)

###################################################################
ExtractBodyFromDir( srcdir, dstdir )
