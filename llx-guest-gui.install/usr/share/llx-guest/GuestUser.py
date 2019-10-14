#!/usr/bin/env python3
# -*- coding: utf-8 -*

import os
import subprocess


script_file_dir="/usr/share/sddm/scripts"
script_file="/usr/share/sddm/scripts/Xsetup.lliurex"
root_script="/root/scripts/guest-account"
DEBUG=True

def printd (text):
	try:
		if DEBUG:
			print("[GuestUser] %s"%text)

	except Exception as e:
		print ("[GuestUser] %s"%e)
		return [False,str(e)]

# def printd


def add_guest_user ():
	
	try:
		if os.path.isfile(script_file):
			os.remove(script_file)

		if not os.path.isdir(script_file_dir):
			os.makedirs(script_file_dir)

		f=open(script_file,"w+")
		f.write("#!/bin/sh\n")
		f.write("# Xsetup - run as root before the login dialog appears\n")
		f.write("%s remove invitado\n"%root_script)
		f.write("%s add\n"%root_script)
		f.close()
		os.chmod(script_file, 0o755)
		printd("File %s has been created"%script_file)
		state=subprocess.Popen("%s add"%root_script, shell=True, stdout=subprocess.PIPE).stdout.read()
		printd("Add user state: %s"%state)
		return [True]
		
	except Exception as e:
		printd("%s"%e)
		return [False,str(e)]

#def add_guest_user



def delete_guest_user ():
	try:
		if os.path.isfile(script_file):
			os.remove(script_file)
			printd("File %s has been removed"%script_file)
		state=subprocess.Popen("%s remove invitado"%root_script, shell=True, stdout=subprocess.PIPE).stdout.read()
		printd("Remove user state: %s"%state)
		return [True]
	except Exception as e:
		printd("%s"%e)
		return [False,str(e)]



#def add_guest_user