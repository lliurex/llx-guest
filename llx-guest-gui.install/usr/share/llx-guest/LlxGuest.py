#!/usr/bin/env python3
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject, GLib, Gdk,Gio

import signal
import gettext
import sys
import threading
import time
import os


signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('llx-guest-gui')
_ = gettext.gettext




class LlxGuest:

	DEBUG= False
	CSS_FILE="/usr/share/llx-guest/rsrc/style.css"

	def printd (self,text):

		if LlxGuest.DEBUG:
			print("[LlxGuestGui] %s"%text)

	# def printd


	def __init__(self):
		
		self.llx_guest_bin="/usr/sbin/llx-guest-gui"
		self.switch_guest_error_state=False
		
		self.start_gui()
		GObject.threads_init()
		Gtk.main()
		
	#def __init__(self):

	def start_gui(self):

		builder=Gtk.Builder()
		builder.set_translation_domain('llx-guest-gui')
		builder.add_from_file("/usr/share/llx-guest/rsrc/llx-guest.ui")
		self.main_window=builder.get_object("main_window")
		self.main_window.set_resizable(False)
		self.main_window.set_icon_from_file('/usr/share/llx-guest/rsrc/llx-guest-icon.svg')
		
		self.main_box=builder.get_object("main_box")
		self.close_button=builder.get_object("close_button")
		self.msg_label=builder.get_object("msg_label")
		self.info_label=builder.get_object("info_label")

		self.switch_guest=builder.get_object("switch_guest")
		self.switch_guest_label=builder.get_object("switch_guest_label")
		
		self.spinner=builder.get_object("spinner")

		self.lock_quit=False
		
		self._set_css_info()
		
		self.switch_initial_state()
		self.connect_signals()
		
		self.main_window.show_all()
		self.spinner.hide()
		#self.msg_label.hide()
		

	#def start_gui

	

	def connect_signals(self):
		
		self.main_window.connect("destroy",self.close_button_clicked)
		#If process is alive destroy window is unable
		self.main_window.connect("delete_event",self.window_close_clicked)
		self.close_button.connect("clicked",self.close_button_clicked)
		self.switch_guest.connect("state_set",self.switch_guest_modify)
		

		
	#def connect_signals


	def switch_initial_state(self):
		
		if self.get_guest_status():
			self.switch_guest.set_state(True)
		
		if not self.check_permissions():
			self.switch_guest.set_sensitive(False)
			self.msg_label.set_text(_("You don't have privileges to enable or disable guest user."))
		
		return True

	# def_switch_initial_state


	def _set_css_info(self):
	
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path(LlxGuest.CSS_FILE)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		
		self.main_window.set_name("WINDOW")
		self.close_button.set_name("CLOSE_BUTTON")
		self.msg_label.set_name("MSG_LABEL")
		self.info_label.set_name("INFO_LABEL")
		
	#def set_css_info	


	def close_button_clicked(self,widget=True):
		
		if self.lock_quit:
			self.msg_label.set_text(_("Please wait until the process is finished"))
			self.msg_label.show()
		else:	
			Gtk.main_quit()
			sys.exit(0)
		
	#def check_changes


	def window_close_clicked(self,widget,event):

		if self.lock_quit:
			self.msg_label.set_text(_("Please wait until the process is finished"))
			self.msg_label.show()
			return True
		else:
			return False
			
	#def unable_quit
	

	def switch_guest_modify(self,widget,gparam):
		if self.switch_guest_error_state:
			return True

			
		self.switch_guest.set_sensitive(False)
		self.close_button.set_sensitive(False)
		self.lock_quit=True
		#self.msg_label.set_name("MSG_LABEL_DELETE")
		self.msg_label.set_text(_("Please wait until the process is finished"))
		self.spinner.show()
		th=threading.Thread(target=self.th_add_guest_user)
		GLib.timeout_add(1000,self.show_reveal,th)
		th.start()
		
		return False

	#def reset_clicked
	
	# ##################### ##########################################
	
	def th_add_guest_user(self,*args):
		self.switch_guest_error_state=False
		if self.switch_guest.get_active():
			self.printd("Adding guest user...")
			#if GuestUser.add_guest_user()[0]:
			if self.enable_guest():
				self.state=True
			else:
				self.state=False
				self.switch_guest_error_state=True
		else:
			self.printd("Deleting guest user...")
			#if GuestUser.delete_guest_user()[0]:
			if self.disable_guest():
				self.state=False
			else:
				self.state=True
				self.switch_guest_error_state=True
				


		#self.printd("Switch was turned %s"%self.state)

		#time.sleep(1)

	def show_reveal(self,*args):
		th=args[-1]
		if th.is_alive():
			self.printd("working, please wait!!")
			return True

		self.printd("Thread FINISHED.")
		
		self.switch_guest.set_sensitive(True)
		self.close_button.set_sensitive(True)
		self.spinner.hide()
		
		self.lock_quit=False
		if self.switch_guest_error_state:
			self.msg_label.set_name("MSG_LABEL")
			self.msg_label.set_text(_("There has been a problem creating guest user."))
			self.switch_guest.set_state(self.state)
		else:
			
			if self.state:
				self.msg_label.set_name("MSG_LABEL")
				self.msg_label.set_text(_("Guest user added."))
			else:
				self.msg_label.set_name("MSG_LABEL")
				self.msg_label.set_text(_("Guest user deleted."))
			
			self.switch_guest_error_state=False
		self.msg_label.show()

		return False

	# ##################### ##########################################



	def get_guest_status(self):
		
		ret=os.system("llx-guest-manager status")
		
		if ret==0:
			return True
		
		
		return False
		
	#def get_guest_state
	
	
	def enable_guest(self):
		
		ret=os.system("llx-guest-manager enable")
		
		if ret==0:
			self.state=True
			return True
		else:
			self.switch_guest_error_state=True
			return False
		
	#def enable_guest
	
	
	def disable_guest(self):
		
		ret=os.system("llx-guest-manager disable")
		
		if ret==0:
			self.state=False
			return True
		else:
			self.switch_guest_error_state=True
			return False
		
	#def disable_user
	
	
	def check_permissions(self):
		
		try:
			f=open("/run/llx-guest.run","w")
			f.close()
			return True
		except:
			return False
		
	#def check_permissions


#class LlxGuest



if __name__=="__main__":
	
	pass
