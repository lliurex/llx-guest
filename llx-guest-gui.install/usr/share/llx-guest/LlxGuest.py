#!/usr/bin/env python3
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject, GLib, Gdk

import signal
import gettext
import sys
import threading
import time
import GuestUser as GuestUser

signal.signal(signal.SIGINT, signal.SIG_DFL)
#gettext.textdomain('lliurex-perfilreset')
_ = gettext.gettext

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

#class spinner


class LlxGuest:

	DEBUG= True

	def printd (self,text):

		if LlxGuest.DEBUG:
			print("[LlxGuestGui] %s"%text)

	# def printd


	def __init__(self):
		
		self.llx_guest_bin="/usr/sbin/llx-guest-gui"
		
		
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
		self.main_window.set_name("WINDOW")
		self.main_box=builder.get_object("main_box")

		self.close_button=builder.get_object("close_button")
		self.close_button.set_name("CLOSE_BUTTON")
		self.msg_label=builder.get_object("msg_label")
		self.msg_label.set_name("MSG_LABEL")

		self.switch_guest=builder.get_object("switch_guest")
		self.switch_guest_label=builder.get_object("switch_guest_label")

		self.reveal=Gtk.Revealer()
		self.reveal.set_name("WHITE_BACKGROUND")
		self.reveal.set_transition_duration(1)

		lbl_rvl=Gtk.Label(_("Generating guest user, please wait..."))
		lbl_rvl.set_name("NOTIF_LABEL")
		lbl_rvl.set_hexpand(False)
		lbl_rvl.set_vexpand(False)
		lbl_rvl.set_halign(Gtk.Align.CENTER)
		lbl_rvl.set_valign(Gtk.Align.CENTER)
		self.reveal.add(lbl_rvl)
		self.main_box.attach(self.reveal,0,0,1,4)

		self.lock_quit=False
		self.switch_initial_state()
		self.connect_signals()
		self._set_css_info()

		self.msg_label.hide()
		self.main_window.show_all()
		

	#def start_gui

	

	def connect_signals(self):
		
		self.main_window.connect("destroy",self.close_button_clicked)
		#If process is alive destroy window is unable
		self.main_window.connect("delete_event",self.unable_quit)
		self.close_button.connect("clicked",self.close_button_clicked)
		self.switch_guest.connect("state_set",self.switch_guest_modify)

		
	#def connect_signals


	def switch_initial_state(self):

		self.state="off"
		self.switch_guest.set_active(False)
		with open("/etc/passwd") as infile:
			for line in infile:
				line = line.rstrip('\n')
				if "invitado" in line:
					self.state="on"
					self.switch_guest.set_active(True)

	# def_switch_initial_state



	def close_button_clicked(self,widget=True):
		
		if self.lock_quit:
			self.msg_label.set_text(_("You must wait to end the process......keep calm."))
			self.printd("You must wait to end the process......keep calm.")
			self.msg_label.show()
		else:	
			Gtk.main_quit()
			sys.exit(0)
		
	#def check_changes

	def switch_guest_modify(self,widget,gparam):

		self.switch_guest.set_sensitive(False)
		self.main_window.connect
		self.lock_quit=True
		self.msg_label.set_name("MSG_LABEL_DELETE")
		self.msg_label.set_text(_("Please wait until the process is finished....."))
		#spinner = Spinner()
		#spinner.start()
		#self.retcode=None
		#self.reveal.set_reveal_child(True)
		th=threading.Thread(target=self.th_add_guest_user)
		GLib.timeout_add(1000,self.show_reveal,th)
		th.start()
		#self.retcode=1
		#spinner.stop()

	#def reset_clicked
	
	# ##################### ##########################################
	
	def th_add_guest_user(self,*args):

		if self.switch_guest.get_active():
			if GuestUser.add_guest_user()[0]:
				self.state="on"
			else:
				self.state="error"
				self.switch_guest_error_state=False
		else:
			self.state = "off"
			if GuestUser.delete_guest_user()[0]:
				self.state="off"
			else:
				self.state="error"
				self.switch_guest_error_state=True
				


		#self.printd("Switch was turned %s"%self.state)

		time.sleep(2)

	def show_reveal(self,*args):
		th=args[-1]
		if th.is_alive():
			self.printd("working!!")
			return True

		self.printd("Thread FINISHED.")

		#spinner.stop()
		#self.reveal.set_reveal_child(False)
		self.switch_guest.set_sensitive(True)
		self.lock_quit=False
		self.switch_guest.set_active(switch_guest_error_state)
		if self.state=="error":
			self.msg_label.set_name("MSG_LABEL")
			self.msg_label.set_text(_("LlX-Guest user has been a problem to modify user files\nPlease contact with the administrator system."))
			self.printd("LlX-Guest user has been a problem to modify user files\nPlease contact with the administrator system.")
		else:
			if self.state=="on":
				self.msg_label.set_name("MSG_LABEL")
				self.msg_label.set_text(_("Guest user added\nYou must restart the session to try it."))
			else:
				self.msg_label.set_name("MSG_LABEL")
				self.msg_label.set_text(_("Guest user deleted"))
		self.msg_label.show()

		return False

	# ##################### ##########################################

	def unable_quit(self,widget,event):

		if self.lock_quit:
			self.msg_label.set_text(_("You must wait to end the process......keep calm."))
			self.printd("You must wait to end the process......keep calm.")
			self.msg_label.show()
			return True
		else:
			return False
			
	#def unable_quit


	def _set_css_info(self):
	
		css = b"""

		GtkLabel {
			font-family: Roboto;
		}

		#WINDOW{
		
		background-color: #ffffff;
		
		}

		#NOTIF_LABEL{
			background: #3366cc;
			font: 11px Roboto;
			color:white;
			border: dashed 1px silver;
			padding:6px;
		}

		#MSG_LABEL {
			color: #24478f;
			font: 11pt Roboto Bold;

		}

		#MSG_LABEL_DELETE {
			color: red;
			font: 11pt Roboto Bold;

		}

		#WHITE_BACKGROUND {
			background: rgba(1,1,1,0);
			box-shadow: 1px 1px 1px 10px white;
		
		}

		#CLOSE_BUTTON{
			border-width: 0px;
			box-shadow: none;
			border-color: #76819a;
			background-image:-gtk-gradient (linear,	left top, left bottom, from (#76819a),  to (#76819a));
			font: 11pt Roboto Light;
			text-shadow: none;
			color: rgba(0,0,0,0.7);
		}
		#CLOSE_BUTTON:hover {
			border-color: #209ddd;
			background-image:-gtk-gradient (linear,	left top, left bottom, from (#209ddd),  to (#209ddd));
			box-shadow: -0.5px 3px 3px #aaaaaa;
			font: 11pt Roboto Light;
			text-shadow: none;
			color: rgba(255,255,255,1);
		}

		"""
		self.style_provider=Gtk.CssProvider()
		self.style_provider.load_from_data(css)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	#def set_css_info		


#class LlxGuest



if __name__=="__main__":
	
	pass