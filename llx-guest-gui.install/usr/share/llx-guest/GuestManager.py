#!/usr/bin/python3

import os
import subprocess
import sys
import shutil

class GuestManager:

	ENABLE_USER_SUCCESSFUL=0
	DISABLE_USER_SUCCESSFUL=1
	USER_ALREADY_ENABLED=2
	USER_ALREADY_DISABLED=3

	APPLY_CHANGES_ENABLE_ERROR=-1
	APPLY_CHANGES_DISABLE_ERROR=-2

	def __init__(self):

		self.debug=False
		self.isGuestUserEnabled=False
		self.getSessionLang()
		self.clearCache()

	#def __init__

	def printd (self,text):

		if self.debug:
			print("[LlxGuestGui] %s"%text)

	# def printd

	def getGuestUserStatus(self):

		ret=os.system("llx-guest-manager status")

		if ret==0:
			self.isGuestUserEnabled=True
		else:
			self.isGuestUserEnabled=False

		self.printd("Get guest user status: %s"%str(ret))

	#def getGuestUserStatus

	def enableGuestUser(self):

		error=False
		msg=""
		
		if not self.isGuestUserEnabled:
			ret=os.system("llx-guest-manager enable")
			self.printd("Enable guest user: %s"%str(ret))

			if ret==0:
				msg=GuestManager.ENABLE_USER_SUCCESSFUL
				self.getGuestUserStatus()
			else:
				error=True
				msg=GuestManager.APPLY_CHANGES_ENABLE_ERROR
		else:
			msg=GuestManager.USER_ALREADY_ENABLED
		
		result=[error,msg]
		return result 	
		
	#def enableGuestUser

	def disableGuestUser(self):

		error=False
		msg=""

		if self.isGuestUserEnabled:
			ret=os.system("llx-guest-manager disable")
			self.printd("Disable guest user: %s"%str(ret))

			if ret==0:
				msg=GuestManager.DISABLE_USER_SUCCESSFUL
				self.getGuestUserStatus()
			else:
				msg=GuestManager.APPLY_CHANGES_DISABLE_ERROR
				error=True
		else:
			msg=GuestManager.USER_ALREADY_DISABLED
			
		result=[error,msg]
		
		return result 	
		
	#def disableGuestUser

	def getSessionLang(self):

		lang=os.environ["LANG"]
		
		if 'valencia' in lang:
			self.sessionLang="ca@valencia"
		else:
			self.sessionLang="es"

	#def getSessionLang

	def clearCache(self):

		clear=False
		
		if "PKEXEC_UID" in os.environ:
			versionFile="/root/.llx-guest.conf"
			cachePath1="/root/.cache/llx-guest-gui"
		else:
			versionFile="/home/%s/.config/llx-guest.conf"%os.environ["USER"]
			cachePath1="/home/%s/.cache/llx-guest-gui"%os.environ["USER"]
		
		installedVersion=self.getPackageVersion()

		try:
			if not os.path.exists(versionFile):
				with open(versionFile,'w') as fd:
					fd.write(installedVersion)

				clear=True

			else:
				with open(versionFile,'r') as fd:
					fileVersion=fd.readline()
					fd.close()

				if fileVersion!=installedVersion:
					with open(versionFile,'w') as fd:
						fd.write(installedVersion)
						fd.close()
					clear=True
		except:
			clear=False
		
		if clear:
			if os.path.exists(cachePath1):
				shutil.rmtree(cachePath1)

	#def clearCache

	def getPackageVersion(self):

		packageVersionFile="/var/lib/llx-guest/version"
		pkgVersion=""

		if os.path.exists(packageVersionFile):
			with open(packageVersionFile,'r') as fd:
				pkgVersion=fd.readline()
				fd.close()

		return pkgVersion

	#def getPackageVersion

#class GuestManager
