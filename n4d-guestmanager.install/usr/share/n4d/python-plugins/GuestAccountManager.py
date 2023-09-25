import os
import subprocess
import pwd
import n4d.responses

class GuestAccountManager:
	
	GUEST_USER="guest-user"
	GUEST_UID=59999
	#GUEST_HOME="/run/%s/home"%GUEST_USER
	GUEST_HOME="/home/%s"%GUEST_USER
	GUEST_PASSWORD="U6aMy0wojraho"
	
	def __init__(self):
		
		self.enabled=False
		self.get_guest_status()
		
		if self.enabled:
			self._check_home_dir()
			
	#def init
	
	
	def startup(self,options):
		
		# already manages if user is enabled
		pass
		
	#def startup
	
	def _check_home_dir(self):
	
		try:
			info=pwd.getpwnam("guest-user")
			if info.pwd_dir != GuestAccountManager.GUEST_HOME:
				os.system("usermod -d %s -m %s 1>/dev/null 2>/dev/null || true"%(GuestAccountManager.GUEST_HOME,GuestAccountManager.GUEST_USER))
		except:
			pass
	
	#def _check_home_dir
	
	
	
	def _run_command(self,command):
		
		ret={}
		command="LC_ALL=C %s"%command
		p=subprocess.Popen([command],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		ret["stdout"],ret["stderr"]=p.communicate()
		ret["returncode"]=p.returncode
		
		return ret
		
	#def _run_command
	
	
	def _build_response(self):
		
		ret={}
		ret["status"]=False
		ret["msg"]=None
	
		return ret
		
	#def _build_response
	
	
	def _set_sddm_button(self,state):
		
		if state:
			#Enabling sddm button
			pass
		else:
			#Disabling sddm button
			pass
		
		return True
		
	#def _set_sddm_button
	
	
	def _disable_password_change(self):
		
		command="passwd -n 1000000 %s"%GuestAccountManager.GUEST_USER
		ret=self._run_command(command)
		
		if ret["returncode"]==0:
			return True
		else:
			return False
		
	#def _disable_password_change
			
	
	def _set_pam_config(self,status=True):
		
		mode="--enable"		
		if not status:
			mode="--remove"
		command="pam-auth-update %s guestuser"%mode
		
		ret=self._run_command(command)
		
		if ret["returncode"]==0:
			return True
		else:
			return False
		
	#def _set_pam_config
	
	
	# ############## #
	# PUBLIC FUNCTIONS   #
	# ############## #
	
	def get_guest_status(self):
		
		ret=self._build_response()
		ret["status"]=False
		
		try:
			guest_user=pwd.getpwnam(GuestAccountManager.GUEST_USER)
			ret["status"]=True
			ret["msg"]="%s is enabled"%(GuestAccountManager.GUEST_USER)
			
		except Exception as e:
			ret["msg"]=str(e)
		
		self.enabled=ret["status"]
			
		#return ret
		return n4d.responses.build_successful_call_response(ret)
		
	#def get_guest_state
	
	
	def fix_guest_password(self):
		
		ret=self._build_response()
		
		if self.enabled:
			command="usermod -p %s %s"%(GuestAccountManager.GUEST_PASSWORD,GuestAccountManager.GUEST_USER)
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="Password changed"
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			self._disable_password_change()
			
		else:

			ret["status"]=False
			ret["msg"]="User does not exist"
			
		#return ret
		return n4d.responses.build_successful_call_response(ret)
		
		
	#def fix_guest_password
	
	
	def enable_guest_user(self):
		
		ret=self._build_response()
		
		if not self.enabled:
		
			command="useradd -p %s -M -N -u %s -r -s /bin/bash -G cdrom,dip,plugdev,sambashare -d %s %s"%(GuestAccountManager.GUEST_PASSWORD,GuestAccountManager.GUEST_UID,GuestAccountManager.GUEST_HOME,GuestAccountManager.GUEST_USER)
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="Guest user created"
				
				self._disable_password_change()
				self._set_pam_config(True)
				self._set_sddm_button(True)
				self.enabled=True
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			return ret
			
		ret["status"]=False
		ret["msg"]="%s already enabled"%GuestAccountManager.GUEST_USER
		
		#return ret
		return n4d.responses.build_successful_call_response(ret)
			
	#def add_guest_user
	
	
	def disable_guest_user(self):
		
		ret=self._build_response()
		
		if self.enabled:
			command="userdel %s"%GuestAccountManager.GUEST_USER
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="%s disabled"%GuestAccountManager.GUEST_USER
				self._set_sddm_button(False)
				self._set_pam_config(False)
				self.enabled=False
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			return ret
			
		ret["status"]=False
		ret["msg"]="%s is not enabled"%GuestAccountManager.GUEST_USER
		
		#return ret
		return n4d.responses.build_successful_call_response(ret)

		
	#def remove_guest_user
	
	
	
#class GuestAccountManager


if __name__=="__main__":
	
	gam=GuestAccountManager()
	print(gam.get_guest_state())
	print(gam.enable_guest_user())
	#print gam.fix_guest_password()
	print(gam.disable_guest_user())
