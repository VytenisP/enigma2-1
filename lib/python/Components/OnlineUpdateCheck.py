from boxbranding import getImageVersion, getImageBuild, getImageDistro, getMachineBrand, getMachineName, getMachineBuild, getImageType

from time import time
from boxbranding import getImageVersion

from enigma import eTimer

import Components.Task
from Components.Ipkg import IpkgComponent
from Components.config import config
from Components.About import about

import urllib2, socket, sys

error = 0

def OnlineUpdateCheck(session=None, **kwargs):
	global onlineupdatecheckpoller
	onlineupdatecheckpoller = OnlineUpdateCheckPoller()
	onlineupdatecheckpoller.start()

class FeedsStatusCheck:
	def __init__(self):
		self.ipkg = IpkgComponent()
		self.ipkg.addCallback(self.ipkgCallback)

	def IsInt(self, val):
		try: 
			int(val)
			return True
		except ValueError:
			return False

	def getFeedSatus(self):
		status = '1'
		trafficLight = 'unknown'

# TODO: Enable traffic status for Obh

#		if about.getIfConfig('eth0').has_key('addr') or about.getIfConfig('eth1').has_key('addr') or about.getIfConfig('wlan0').has_key('addr') or about.getIfConfig('ra0').has_key('addr'):
#			try:
#
#				print '[OnlineVersionCheck] Checking feeds state'
#				req = urllib2.Request('http://www.vuplus-community.net/TrafficLightState.php')
#				d = urllib2.urlopen(req)
#				trafficLight = d.read()
#			except urllib2.HTTPError, err:
#				print '[OnlineVersionCheck] ERROR:',err
#				trafficLight = err.code
#			except urllib2.URLError, err:
#				print '[OnlineVersionCheck] ERROR:',err.reason[0]
#				trafficLight = err.reason[0]
#			except urllib2, err:
#				print '[OnlineVersionCheck] ERROR:',err
#				trafficLight = err
#			except:
#				print '[OnlineVersionCheck] ERROR:', sys.exc_info()[0]
#				trafficLight = -2
#			if not self.IsInt(trafficLight) and getImageType() != 'release':
#				trafficLight = 'unknown'
#			elif trafficLight == 'stable':
#				status = '0'
#			config.softwareupdate.updateisunstable.setValue(status)
#			print '[OnlineVersionCheck] PASSED:',trafficLight
#			return trafficLight
#		else:
#			print '[OnlineVersionCheck] ERROR: -2'
#			return -2

# HACK OBH
		trafficLight = 'stable'
		status = '0'
		config.softwareupdate.updateisunstable.setValue(status)
		return trafficLight
# END
	def getFeedsBool(self):
		global error
		feedstatus = feedsstatuscheck.getFeedSatus()
		if feedstatus in (-2, 403, 404):
			print '[OnlineVersionCheck] Error %s' % feedstatus
			return feedstatus
		elif error:
			print '[OnlineVersionCheck] Check already in progress'
			return 'inprogress'
		elif feedstatus == 'updating':
			print '[OnlineVersionCheck] Feeds Updating'
			return 'updating'
		elif feedstatus in ('stable', 'unstable', 'unknown'):
			print '[OnlineVersionCheck]',feedstatus.title()
			return str(feedstatus)

	def getFeedsErrorMessage(self):
		global error
		feedstatus = feedsstatuscheck.getFeedsBool()
		if feedstatus == -2:
			return _("Your %s %s has no network access, please check your network settings and make sure you have network cable connected and try again.") % (getMachineBrand(), getMachineName())
		elif feedstatus == 404:
			return _("Your %s %s is not connected to the internet, please check your network settings and try again.") % (getMachineBrand(), getMachineName())
		elif feedstatus in ('updating', 403):
			return _("Sorry feeds are down for maintenance, please try again later. If this issue persists please check vuplus-community.net.")
		elif error:
			return _("There has been an error, please try again later. If this issue persists, please check vuplus-community.net")

	def startCheck(self):
		global error
		error = 0
		self.updating = True
		self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)

	def ipkgCallback(self, event, param):
		config.softwareupdate.updatefound.setValue(False)
		if event == IpkgComponent.EVENT_ERROR:
			global error
			error += 1
		elif event == IpkgComponent.EVENT_DONE:
			if self.updating:
				self.updating = False
				self.ipkg.startCmd(IpkgComponent.CMD_UPGRADE_LIST)
			elif self.ipkg.currentCommand == IpkgComponent.CMD_UPGRADE_LIST:
				self.total_packages = len(self.ipkg.getFetchedList())
				if self.total_packages and (getImageType() != 'release' or (config.softwareupdate.updateisunstable.value == '1' and config.softwareupdate.updatebeta.value) or config.softwareupdate.updateisunstable.value == '0'):
					print ('[OnlineVersionCheck] %s Updates available' % self.total_packages)
					config.softwareupdate.updatefound.setValue(True)
		pass
		

feedsstatuscheck = FeedsStatusCheck()

class OnlineUpdateCheckPoller:
	def __init__(self):
		# Init Timer
		self.timer = eTimer()

	def start(self):
		if self.onlineupdate_check not in self.timer.callback:
			self.timer.callback.append(self.onlineupdate_check)

		if time() > 1262304000:
			self.timer.startLongTimer(0)
		else:
			self.timer.startLongTimer(120)

	def stop(self):
		if self.version_check in self.timer.callback:
			self.timer.callback.remove(self.onlineupdate_check)
		self.timer.stop()

	def onlineupdate_check(self):
		if config.softwareupdate.check.value:
			Components.Task.job_manager.AddJob(self.createCheckJob())
		self.timer.startLongTimer(config.softwareupdate.checktimer.value * 3600)

	def createCheckJob(self):
		job = Components.Task.Job(_("OnlineVersionCheck"))
		task = Components.Task.PythonTask(job, _("Checking for Updates..."))
		task.work = self.JobStart
		task.weighting = 1
		return job

	def JobStart(self):
		config.softwareupdate.updatefound.setValue(False)
		if (getImageType() != 'release' and feedsstatuscheck.getFeedsBool() == 'unknown') or (getImageType() == 'release' and feedsstatuscheck.getFeedsBool() in ('stable', 'unstable')):
			print '[OnlineVersionCheck] Starting background check.'
			feedsstatuscheck.startCheck()
		else:
			print '[OnlineVersionCheck] No feeds found, skipping check.'


class VersionCheck:
	def __init__(self):
		pass

	def getStableUpdateAvailable(self):
		if config.softwareupdate.updatefound.value and config.softwareupdate.check.value:
			if getImageType() != 'release' or config.softwareupdate.updateisunstable.value == '0':
				print '[OnlineVersionCheck] New Release updates found'
				return True
			else:
				print '[OnlineVersionCheck] skipping as unstable is not wanted'
				return False
		else:
			return False

	def getUnstableUpdateAvailable(self):
		if config.softwareupdate.updatefound.value and config.softwareupdate.check.value:
			if getImageType() != 'release' or (config.softwareupdate.updateisunstable.value == '1' and config.softwareupdate.updatebeta.value):
				print '[OnlineVersionCheck] New Experimental updates found'
				return True
			else:
				print '[OnlineVersionCheck] skipping as beta is not wanted'
				return False
		else:
			return False

versioncheck = VersionCheck()
