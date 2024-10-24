#!/usr/bin/python3

from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time
import pwd
import GuestManager

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	#def __init__
		

	def run(self,*args):
		
		time.sleep(1)
		LlxGuest.guestMan.getGuestUserStatus()

	#def run

#class GatherInfo

class SetChanges(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.newValue=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		if self.newValue:
			self.ret=LlxGuest.guestMan.enableGuestUser()
		else:
			self.ret=LlxGuest.guestMan.disableGuestUser()

	#def run

#class SetChanges

class LlxGuest(QObject):

	guestMan=GuestManager.GuestManager()

	def __init__(self):

		QObject.__init__(self)
		self.initBridge()

	#def __init__

	def initBridge(self):

		self._isGuestUserEnabled=False
		self._settingsChanged=False
		self._showSettingsMessage=[False,"","Success"]
		self._closeGui=False
		self._closePopUp=True
		self._showChangesDialog=False
		self._currentStack=0
		self._currentOptionsStack=0
		self.correctCode=True
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge

	def _loadConfig(self):		

		self._isGuestUserEnabled=LlxGuest.guestMan.isGuestUserEnabled
		self.currentStack=1

	#def _loadConfig

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack

	def _setCurrentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurrentStack

	def _getCurrentOptionsStack(self):

		return self._currentOptionsStack

	#def _getCurrentOptionsStack

	def _setCurrentOptionsStack(self,currentOptionsStack):

		if self._currentOptionsStack!=currentOptionsStack:
			self._currentOptionsStack=currentOptionsStack
			self.on_currentOptionsStack.emit()

	#def _setCurrentOptionsStack

	def _getIsGuestUserEnabled(self):

		return self._isGuestUserEnabled

	#def _getIsGuestUserEnabled

	def _setIsGuestUserEnabled(self,isGuestUserEnabled):

		if self._isGuestUserEnabled!=isGuestUserEnabled:
			self._isGuestUserEnabled=isGuestUserEnabled
			self.on_isGuestUserEnabled.emit()

	#def _setIsGuestUserEnabled

	def _getSettingsChanged(self):

		return self._settingsChanged

	#def _getSettingsChanged

	def _setSettingsChanged(self,settingsChanged):

		if self._settingsChanged!=settingsChanged:
			self._settingsChanged=settingsChanged
			self.on_settingsChanged.emit()

	#def _setSettingsChanged

	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage

	def _setShowSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowChangesDialog(self):

		return self._showChangesDialog

	#def _getShowChangesDialog

	def _setShowChangesDialog(self,showChangesDialog):

		if self._showChangesDialog!=showChangesDialog:
			self._showChangesDialog=showChangesDialog
			self.on_showChangesDialog.emit()

	#def _setShowChangesDialog

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp	

	def _setClosePopUp(self,closePopUp):
		
		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp		
			self.on_closePopUp.emit()

	#def _setClosePopUp	

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui		
			self.on_closeGui.emit()

	#def _setCloseGui	

	@Slot(bool)
	def manageChanges(self,value):

		self.showSettingsMessage=[False,"","Success"]
		
		if value!=self.isGuestUserEnabled:
			self.isGuestUserEnabled=value
			if self.isGuestUserEnabled!=LlxGuest.guestMan.isGuestUserEnabled:
				self.settingsChanged=True
			else:
				self.settingsChanged=False
					
	#def manageChanges

	@Slot()
	def applyChanges(self):

		self.showSettingsMessage=[False,"","Success"]
		self.closePopUp=False
		self.showChangesDialog=False
		self.setChangesT=SetChanges(self.isGuestUserEnabled)
		self.setChangesT.start()
		self.setChangesT.finished.connect(self._applyChanges)

	#def applyChanges	

	def _applyChanges(self):

		if not self.setChangesT.ret[0]:
			self.showSettingsMessage=[True,self.setChangesT.ret[1],"Success"]
			self.closeGui=True
		else:
			self.showSettingsMessage=[True,self.setChangesT.ret[1],"Error"]
			self.closeGui=False

		self.isGuestUserEnabled=LlxGuest.guestMan.isGuestUserEnabled
		self.settingsChanged=False
		self.closePopUp=True

	#def _applyChanges

	@Slot()
	def cancelChanges(self):

		self.showSettingsMessage=[False,"","Success"]
		self.closePopUp=False
		self.closeGui=False
		self.showChangesDialog=False
		self._cancelChanges()

	#def cancelGroupChanges

	def _cancelChanges(self):

		self.isGuestUserEnabled=LlxGuest.guestMan.isGuestUserEnabled
		self.settingsChanged=False
		self.closePopUp=True
		self.closeGui=True

	#def _cancelGroupChanges

	@Slot(str)
	def manageSettingsDialog(self,action):
		
		if action=="Accept":
			self.applyChanges()
		elif action=="Discard":
			self.cancelChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showChangesDialog=False

	#def manageSettingsDialog

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.currentOptionsStack=stack

	#def manageTransitions
	
	@Slot()
	def openHelp(self):
		
		runPkexec=False
		
		if "PKEXEC_UID" in os.environ:
			runPkexec=True

		if 'valencia' in LlxGuest.guestMan.sessionLang:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Activa%20compte%20d%27usuari%20convidat%20en%20LliureX%2021'
		else:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Activar+cuenta+de+usuario+invitado+en+LliureX+21'
		
		if not runPkexec:
			self.helpCmd="su -c '%s' $USER"%self.helpCmd
		else:
			user=pwd.getpwuid(int(os.environ["PKEXEC_UID"])).pw_name
			self.helpCmd="su -c '%s' %s"%(self.helpCmd,user)

		self.openHelp_t=threading.Thread(target=self._openHelp)
		self.openHelp_t.daemon=True
		self.openHelp_t.start()

	#def openHelp

	def _openHelp(self):

		os.system(self.helpCmd)

	#def _openHelp

	@Slot()
	def closeApplication(self):

		self.closeGui=False
		if self.settingsChanged:
			self.showChangesDialog=True
		else:
			self.closeGui=True

	#def closeApplication
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack, notify=on_currentOptionsStack)

	on_isGuestUserEnabled=Signal()
	isGuestUserEnabled=Property(bool,_getIsGuestUserEnabled,_setIsGuestUserEnabled,notify=on_isGuestUserEnabled)
	
	on_settingsChanged=Signal()
	settingsChanged=Property(bool,_getSettingsChanged,_setSettingsChanged, notify=on_settingsChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	on_showChangesDialog=Signal()
	showChangesDialog=Property(bool,_getShowChangesDialog,_setShowChangesDialog, notify=on_showChangesDialog)

#class LlxGuest

