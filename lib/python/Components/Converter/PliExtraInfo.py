# shamelessly copied from pliExpertInfo (Vali, Mirakels, Littlesat)

from os import path
from enigma import iServiceInformation, iPlayableService
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Tools.Transponder import ConvertToHumanReadable, getChannelNumber
from Tools.GetEcmInfo import GetEcmInfo
from Poll import Poll

def addspace(text):
	if text:
		text += "  "
	return text

class PliExtraInfo(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True
		self.caid_data = (
			("0x1700", "0x17ff", "BetaCrypt",      "B",  True ),
			( "0x600",  "0x6ff", "Irdeto",         "I",  True ),
			("0x1800", "0x18ff", "Nagravision",    "N",  True ),
			( "0x100",  "0x1ff", "Seca Mediaguard","S",  True ),
			("0x1000", "0x10FF", "Tandberg",       "T",  True ),
			( "0x500",  "0x5ff", "Viaccess",       "V",  True ),
			("0x2600", "0x2600", "Biss",           "BI", True ),
			("0x4aee", "0x4aee", "BulCrypt",       "BU", True ),
			("0x5581", "0x5581", "BulCrypt",       "BU", False),
			( "0xb00",  "0xbff", "Conax",          "CO", True ),
			( "0xd00",  "0xdff", "CryptoWorks",    "CW", True ),
			("0x4ae0", "0x4ae1", "DRE-Crypt",      "DC", True ),
			( "0x900",  "0x9ff", "NDS Videoguard", "ND", True ),
			( "0xe00",  "0xeff", "PowerVu",        "PV", True ),
		)
		self.ca_table = (
			("CryptoCaidBetatAvailable",    "B",	False),
			("CryptoCaidIrdetoAvailable"    "I",	False),
			("CryptoCaidNagraAvailable",    "N",	False),
			("CryptoCaidSecaAvailable",     "S",	False),
			("CryptoCaidTandbergAvailable", "T",	False),
			("CryptoCaidViaAvailable",      "V",	False),
			("CryptoCaidBissAvailable",	    "BI",	False),
			("CryptoCaidBulCrypt1Available","BU",	False),
			("CryptoCaidBulCrypt2Available","BU",	False),
			("CryptoCaidConaxAvailable",    "CO",	False),
			("CryptoCaidCryptoWAvailable",  "CW",	False),
			("CryptoCaidDreAvailable",      "DC",	False),
			("CryptoCaidNDSAvailable",      "ND",	False),
			("CryptoCaidPowerVuAvailable",  "PV",	False),
			("CryptoCaidBetaSelected",      "B",	True ),
			("CryptoCaidIrdetoSelected",    "I",	True ),
			("CryptoCaidNagraSelected",     "N",	True ),
			("CryptoCaidSecaSelected",      "S",	True ),
			("CryptoCaidTandbergSelected",  "T",	True ),
			("CryptoCaidViaSelected",       "V",	True ),
			("CryptoCaidBissSelected",      "BI",	True ),
			("CryptoCaidBulCrypt1Selected", "BU",	True ),
			("CryptoCaidBulCrypt2Selected", "BU",	True ),
			("CryptoCaidConaxSelected",     "CO",	True ),
			("CryptoCaidCryptoWSelected",   "CW",	True ),
			("CryptoCaidDreSelected",       "DC",	True ),
			("CryptoCaidNDSSelected",       "ND",	True ),
			("CryptoCaidPowerVuSelected",   "PV",	True ),
		)
		self.ecmdata = GetEcmInfo()
		self.feraw = self.fedata = self.updateFEdata = None

	def getCryptoInfo(self, info):
		if info.getInfo(iServiceInformation.sIsCrypted) == 1:
			data = self.ecmdata.getEcmData()
			self.current_source = data[0]
			self.current_caid = data[1]
			self.current_provid = data[2]
			self.current_ecmpid = data[3]
		else:
			self.current_source = ""
			self.current_caid = "0"
			self.current_provid = "0"
			self.current_ecmpid = "0"

	def createCryptoBar(self, info):
		res = ""
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)

		for caid_entry in self.caid_data:
			if int(caid_entry[0], 16) <= int(self.current_caid, 16) <= int(caid_entry[1], 16):
				color="\c0000??00"
			else:
				color = "\c007?7?7?"
				try:
					for caid in available_caids:
						if int(caid_entry[0], 16) <= caid <= int(caid_entry[1], 16):
							color="\c00????00"
				except:
					pass

			if color != "\c007?7?7?" or caid_entry[4]:
				if res: res += " "
				res += color + caid_entry[3]

		res += "\c00??????"
		return res

	def createCryptoBeta(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x1700', 16) <= int(self.current_caid, 16) <= int('0x17ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x1700', 16) <= caid <= int('0x17ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'B'
		res += "\c00??????"
		return res

	def createCryptoIrdeto(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x600', 16) <= int(self.current_caid, 16) <= int('0x6ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x600', 16) <= caid <= int('0x6ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'I'
		res += "\c00??????"
		return res

	def createCryptoNagra(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x1800', 16) <= int(self.current_caid, 16) <= int('0x18ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x1800', 16) <= caid <= int('0x18ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'N'
		res += "\c00??????"
		return res

	def createCryptoSeca(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x100', 16) <= int(self.current_caid, 16) <= int('0x1ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x100', 16) <= caid <= int('0x1ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'S'
		res += "\c00??????"
		return res

	def createCryptoTandberg(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x1010', 16) <= int(self.current_caid, 16) <= int('0x1010', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x1010', 16) <= caid <= int('0x1010', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'T'
		res += "\c00??????"
		return res

	def createCryptoVia(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x500', 16) <= int(self.current_caid, 16) <= int('0x5ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x500', 16) <= caid <= int('0x5ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'V'
		res += "\c00??????"
		return res

	def createCryptoBiss(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x2600', 16) <= int(self.current_caid, 16) <= int('0x26ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x2600', 16) <= caid <= int('0x26ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'BI'
		res += "\c00??????"
		return res

	def createCryptoBulCrypt1(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x4aee', 16) <= int(self.current_caid, 16) <= int('0x4aee', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x4aee', 16) <= caid <= int('0x4aee', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'BU'
		res += "\c00??????"
		return res

	def createCryptoBulCrypt2(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x5581', 16) <= int(self.current_caid, 16) <= int('0x5581', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x5581', 16) <= caid <= int('0x5581', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'BU'
		res += "\c00??????"
		return res

	def createCryptoConax(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0xb00', 16) <= int(self.current_caid, 16) <= int('0xbff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0xb00', 16) <= caid <= int('0xbff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'CO'
		res += "\c00??????"
		return res

	def createCryptoCryptoW(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0xd00', 16) <= int(self.current_caid, 16) <= int('0xdff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0xd00', 16) <= caid <= int('0xdff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'CW'
		res += "\c00??????"
		return res

	def createCryptoDre(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x4ae0', 16) <= int(self.current_caid, 16) <= int('0x4ae1', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x4ae0', 16) <= caid <= int('0x4ae1', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'DC'
		res += "\c00??????"
		return res

	def createCryptoNDS(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0x900', 16) <= int(self.current_caid, 16) <= int('0x9ff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0x900', 16) <= caid <= int('0x9ff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'NDS'
		res += "\c00??????"
		return res

	def createCryptoPowerVU(self, info):
		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if int('0xe00', 16) <= int(self.current_caid, 16) <= int('0xeff', 16):
			color="\c004c7d3f"
		else:
			color = "\c009?9?9?"
			try:
				for caid in available_caids:
					if int('0xe00', 16) <= caid <= int('0xeff', 16):
						color="\c00eeee00"
			except:
				pass
		res = color + 'PV'
		res += "\c00??????"
		return res

	def createCryptoSpecial(self, info):
		caid_name = "Free to Air"
		try:
			for caid_entry in self.caid_data:
				if int(caid_entry[0], 16) <= int(self.current_caid, 16) <= int(caid_entry[1], 16):
					caid_name = caid_entry[2]
					break
			return caid_name + ":%04x:%04x:%04x" % (int(self.current_caid,16), int(self.current_provid,16), info.getInfo(iServiceInformation.sSID))
		except:
			pass
		return ""

	def createResolution(self, info):
		video_height = 0
		video_width = 0
		video_pol = " "
		video_rate = 0
		if path.exists("/proc/stb/vmpeg/0/yres"):
			f = open("/proc/stb/vmpeg/0/yres", "r")
			try:
				video_height = int(f.read(),16)
			except:
				pass
			f.close()
		if path.exists("/proc/stb/vmpeg/0/xres"):
			f = open("/proc/stb/vmpeg/0/xres", "r")
			try:
				video_width = int(f.read(),16)
			except:
				pass
			f.close()
		if path.exists("/proc/stb/vmpeg/0/progressive"):
			f = open("/proc/stb/vmpeg/0/progressive", "r")
			try:
				video_pol = "p" if int(f.read(),16) else "i"
			except:
				pass
			f.close()
		if path.exists("/proc/stb/vmpeg/0/framerate"):
			f = open("/proc/stb/vmpeg/0/framerate", "r")
			try:
				video_rate = int(f.read())
			except:
				pass
			f.close()

		fps  = str((video_rate + 500) / 1000)
		return str(video_width) + "x" + str(video_height) + video_pol + fps

	def createVideoCodec(self, info):
		return ("MPEG2", "MPEG4 H.264", "MPEG1", "MPEG4-VC", "VC1", "VC1-SM", "HEVC H.265", "")[info.getInfo(iServiceInformation.sVideoType)]

	def createServiceRef(self, info):
		return info.getInfoString(iServiceInformation.sServiceref)

	def createPIDInfo(self, info):
		vpid = info.getInfo(iServiceInformation.sVideoPID)
		apid = info.getInfo(iServiceInformation.sAudioPID)
		pcrpid = info.getInfo(iServiceInformation.sPCRPID)
		sidpid = info.getInfo(iServiceInformation.sSID)
		tsid = info.getInfo(iServiceInformation.sTSID)
		onid = info.getInfo(iServiceInformation.sONID)
		if vpid < 0 : vpid = 0
		if apid < 0 : apid = 0
		if pcrpid < 0 : pcrpid = 0
		if sidpid < 0 : sidpid = 0
		if tsid < 0 : tsid = 0
		if onid < 0 : onid = 0
		return "%d-%d:%05d:%04d:%04d:%04d" % (onid, tsid, sidpid, vpid, apid, pcrpid)

	def createTransponderInfo(self, fedata, feraw):
		if "DVB-T" in feraw.get("tuner_type"):
			tmp = addspace(self.createChannelNumber(fedata, feraw)) + addspace(self.createFrequency(fedata)) + addspace(self.createPolarization(fedata))
		else:
			tmp = addspace(self.createFrequency(fedata)) + addspace(self.createPolarization(fedata))
		return addspace(self.createTunerSystem(fedata)) + tmp + addspace(self.createSymbolRate(fedata, feraw)) + addspace(self.createFEC(fedata, feraw)) \
			+ addspace(self.createModulation(fedata)) + addspace(self.createOrbPos(feraw))

	def createFrequency(self, fedata):
		frequency = fedata.get("frequency")
		if frequency:
			return str(frequency)
		return ""

	def createChannelNumber(self, fedata, feraw):
		return "DVB-T" in feraw.get("tuner_type") and fedata.get("channel") or ""

	def createSymbolRate(self, fedata, feraw):
		if "DVB-T" in feraw.get("tuner_type"):
			bandwidth = fedata.get("bandwidth")
			if bandwidth:
				return bandwidth
		else:
			symbolrate = fedata.get("symbol_rate")
			if symbolrate:
				return str(symbolrate)
		return ""

	def createPolarization(self, fedata):
		return fedata.get("polarization_abbreviation") or ""

	def createFEC(self, fedata, feraw):
		if "DVB-T" in feraw.get("tuner_type"):
			code_rate_lp = fedata.get("code_rate_lp")
			code_rate_hp = fedata.get("code_rate_hp")
			if code_rate_lp and code_rate_hp:
				return code_rate_lp + "-" + code_rate_hp
		else:
			fec = fedata.get("fec_inner")
			if fec:
				return fec
		return ""

	def createModulation(self, fedata):
		if fedata.get("tuner_type") == _("Terrestrial"):
			constellation = fedata.get("constellation")
			if constellation:
				return constellation
		else:
			modulation = fedata.get("modulation")
			if modulation:
				return modulation
		return ""

	def createTunerType(self, feraw):
		return feraw.get("tuner_type") or ""

	def createTunerSystem(self, fedata):
		return fedata.get("system") or ""

	def createOrbPos(self, feraw):
		orbpos = feraw.get("orbital_position")
		if orbpos > 1800:
			return str((float(3600 - orbpos)) / 10.0) + "\xc2\xb0 W"
		elif orbpos > 0:
			return str((float(orbpos)) / 10.0) + "\xc2\xb0 E"
		return ""

	def createOrbPosOrTunerSystem(self, fedata,feraw):
		orbpos = self.createOrbPos(feraw)
		if orbpos is not "":
			return orbpos
		return self.createTunerSystem(fedata)

	def createTransponderName(self,feraw):
		orbpos = feraw.get("orbital_position")
		if orbpos is None: # Not satellite
			return ""
		freq = feraw.get("frequency")
		if freq and freq < 10700000: # C-band
			if orbpos > 1800:
				orbpos += 1
			else:
				orbpos -= 1
				
		sat_names = {
			30:   'Rascom/Eutelsat 3E',
			48:   'SES 5',
			70:   'Eutelsat 7E',
			90:   'Eutelsat 9E',
			100:  'Eutelsat 10E',  
			130:  'Hot Bird',
			160:  'Eutelsat 16E',
			192:  'Astra 1KR/1L/1M/1N',
			200:  'Arabsat 20E',
			216:  'Eutelsat 21.5E',
			235:  'Astra 3',
			255:  'Eutelsat 25.5E',
			260:  'Badr 4/5/6',
			282:  'Astra 2E/2F/2G',
			305:  'Arabsat 30.5E',
			315:  'Astra 5',
			330:  'Eutelsat 33E',
			360:  'Eutelsat 36E',
			380:  'Paksat',
			390:  'Hellas Sat',
			400:  'Express 40E',
			420:  'Turksat',
			450:  'Intelsat 45E',
			480:  'Afghansat',
			490:  'Yamal 49E',
			530:  'Express 53E',
			570:  'NSS 57E',
			600:  'Intelsat 60E',
			620:  'Intelsat 62E',
			685:  'Intelsat 68.5E',
			705:  'Eutelsat 70.5E',
			720:  'Intelsat 72E',
			750:  'ABS',
			765:  'Apstar',
			785:  'ThaiCom',
			800:  'Express 80E',
			830:  'Insat',
			851:  'Intelsat/Horizons',
			880:  'ST2',
			900:  'Yamal 90E',
			915:  'Mesat',
			950:  'NSS/SES 95E',
			1005: 'AsiaSat 100E',
			1030: 'Express 103E',
			1055: 'Asiasat 105E',
			1082: 'NSS/SES 108E',
			1100: 'BSat/NSAT',
			1105: 'ChinaSat',
			1130: 'KoreaSat',
			1222: 'AsiaSat 122E',
			1380: 'Telstar 18',
			1440: 'SuperBird',
			2310: 'Ciel',
			2390: 'Echostar/Galaxy 121W',
			2410: 'Echostar/DirectTV 119W',
			2500: 'Echostar/DirectTV 110W',
			2630: 'Galaxy 97W',
			2690: 'NIMIQ 91W',
			2780: 'NIMIQ 82W',
			2830: 'Echostar/QuetzSat',
			2880: 'AMC 72W',
			2900: 'Star One',
			2985: 'Echostar 61.5W',
			2990: 'Amazonas',
			3020: 'Intelsat 58W',
			3045: 'Intelsat 55.5W',
			3070: 'Intelsat 53W',
			3100: 'Intelsat 50W',
			3150: 'Intelsat 45W',
			3169: 'Intelsat 43.1W',
			3195: 'SES 40.5W',
			3225: 'NSS/Telstar 37W',
			3255: 'Intelsat 34.5W',
			3285: 'Intelsat 31.5W',
			3300: 'Hispasat',
			3325: 'Intelsat 27.5W',
			3355: 'Intelsat 24.5W',
			3380: 'SES 22W',
			3400: 'NSS 20W',
			3420: 'Intelsat 18W',
			3450: 'Telstar 15W',
			3460: 'Express 14W',
			3475: 'Eutelsat 12.5W',
			3490: 'Express 11W',
			3520: 'Eutelsat 8W',
			3530: 'Nilesat/Eutelsat 7W',
			3550: 'Eutelsat 5W',
			3560: 'Amos',
			3592: 'Thor/Intelsat'
		}
		
		if orbpos in sat_names:
			return sat_names[orbpos]
		elif orbpos > 1800:
			return str((float(3600 - orbpos)) / 10.0) + "W"
		else:
			return str((float(orbpos)) / 10.0) + "E"

	def createProviderName(self,info):
		return info.getInfoString(iServiceInformation.sProvider)

	@cached
	def getText(self):
		service = self.source.service
		if service is None:
			return ""
		info = service and service.info()

		if not info:
			return ""

		if self.type == "CryptoInfo":
			self.getCryptoInfo(info)
			if int(config.usage.show_cryptoinfo.value) > 0:
				return addspace(self.createCryptoBar(info)) + self.createCryptoSpecial(info)
			else:
				return addspace(self.createCryptoBar(info)) + addspace(self.current_source) + self.createCryptoSpecial(info)

		if self.type == "CryptoBar":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoBar(info)
			else:
				return ""

		if self.type == "CryptoBeta":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoBeta(info)
			else:
				return ""

		if self.type == "CryptoIrdeto":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoIrdeto(info)
			else:
				return ""

		if self.type == "CryptoNagra":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoNagra(info)
			else:
				return ""

		if self.type == "Seca":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoSeca(info)
			else:
				return ""

		if self.type == "CryptoTandberg":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoTandberg(info)
			else:
				return ""				

		if self.type == "CryptoVia":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoVia(info)
			else:
				return ""

		if self.type == "CryptoBiss":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoBiss(info)
			else:
				return ""

		if self.type == "CryptoBulCrypt":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoBulCrypt(info)
			else:
				return ""

		if self.type == "CryptoConax":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoConax(info)
			else:
				return ""

		if self.type == "CryptoCryptoW":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoCryptoW(info)
			else:
				return ""

		if self.type == "CryptoDre":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoDre(info)
			else:
				return ""

		if self.type == "CryptoNDS":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoNDS(info)
			else:
				return ""

		if self.type == "CryptoPowerVu":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoPowerVu(info)
			else:
				return ""

		if self.type == "CryptoSpecial":
			if int(config.usage.show_cryptoinfo.value) > 0:
				self.getCryptoInfo(info)
				return self.createCryptoSpecial(info)
			else:
				return ""

		if self.type == "ResolutionString":
			return self.createResolution(info)

		if self.type == "VideoCodec":
			return self.createVideoCodec(info)

		if self.updateFEdata:
			feinfo = service.frontendInfo()
			if feinfo:
				self.feraw = feinfo.getAll(config.usage.infobar_frontend_source.value == "settings")
				if self.feraw:
					self.fedata = ConvertToHumanReadable(self.feraw)

		feraw = self.feraw
		if not feraw:
			feraw = info.getInfoObject(iServiceInformation.sTransponderData)
			if not feraw:
				return ""
			fedata = ConvertToHumanReadable(feraw)
		else:
			fedata = self.fedata
		if self.type == "All":
			self.getCryptoInfo(info)
			if int(config.usage.show_cryptoinfo.value) > 0:
				return addspace(self.createProviderName(info)) + self.createTransponderInfo(fedata,feraw) + addspace(self.createTransponderName(feraw)) + "\n"\
				+ addspace(self.createCryptoBar(info)) + addspace(self.createCryptoSpecial(info)) + "\n"\
				+ addspace(self.createPIDInfo(info)) + addspace(self.createVideoCodec(info)) + self.createResolution(info)
			else:
				return addspace(self.createProviderName(info)) + self.createTransponderInfo(fedata,feraw) + addspace(self.createTransponderName(feraw)) + "\n" \
				+ addspace(self.createCryptoBar(info)) + self.current_source + "\n" \
				+ addspace(self.createCryptoSpecial(info)) + addspace(self.createVideoCodec(info)) + self.createResolution(info)

		if self.type == "ServiceInfo":
			return addspace(self.createProviderName(info)) + addspace(self.createTunerSystem(fedata)) + addspace(self.createFrequency(feraw)) + addspace(self.createPolarization(fedata)) \
			+ addspace(self.createSymbolRate(fedata, feraw)) + addspace(self.createFEC(fedata, feraw)) + addspace(self.createModulation(fedata)) + addspace(self.createOrbPos(feraw)) + addspace(self.createTransponderName(feraw))\
			+ addspace(self.createVideoCodec(info)) + self.createResolution(info)

		if self.type == "TransponderInfo2line":
			return addspace(self.createProviderName(info)) + addspace(self.createTunerSystem(fedata)) + addspace(self.createTransponderName(feraw)) + '\n'\
			+ addspace(self.createFrequency(fedata)) + addspace(self.createPolarization(fedata))\
			+ addspace(self.createSymbolRate(fedata, feraw)) + self.createModulation(fedata) + '-' + addspace(self.createFEC(fedata, feraw))

		if self.type == "PIDInfo":
			return self.createPIDInfo(info)
			
		if self.type == "ServiceRef":
			return self.createServiceRef(info)			

		if not feraw:
			return ""

		if self.type == "TransponderInfo":
			return self.createTransponderInfo(fedata, feraw)

		if self.type == "TransponderFrequency":
			return self.createFrequency(feraw)

		if self.type == "TransponderSymbolRate":
			return self.createSymbolRate(fedata, feraw)

		if self.type == "TransponderPolarization":
			return self.createPolarization(fedata)

		if self.type == "TransponderFEC":
			return self.createFEC(fedata, feraw)

		if self.type == "TransponderModulation":
			return self.createModulation(fedata)

		if self.type == "OrbitalPosition":
			return self.createOrbPos(feraw)

		if self.type == "TunerType":
			return self.createTunerType(feraw)

		if self.type == "TunerSystem":
			return self.createTunerSystem(fedata)

		if self.type == "OrbitalPositionOrTunerSystem":
			return self.createOrbPosOrTunerSystem(fedata,feraw)

		if self.type == "TerrestrialChannelNumber":
			return self.createChannelNumber(fedata, feraw)

		return _("invalid type")

	text = property(getText)

	@cached
	def getBool(self):
		service = self.source.service
		info = service and service.info()

		if not info:
			return False

		request_caid = None
		for x in self.ca_table:
			if x[0] == self.type:
				request_caid = x[1]
				request_selected = x[2]
				break

		if request_caid is None:
			return False

		if info.getInfo(iServiceInformation.sIsCrypted) != 1:
			return False

		data = self.ecmdata.getEcmData()

		if data is None:
			return False

		current_caid	= data[1]

		available_caids = info.getInfoObject(iServiceInformation.sCAIDs)

		for caid_entry in self.caid_data:
			if caid_entry[3] == request_caid:
				if request_selected:
					if int(caid_entry[0], 16) <= int(current_caid, 16) <= int(caid_entry[1], 16):
						return True
				else: # request available
					try:
						for caid in available_caids:
							if int(caid_entry[0], 16) <= caid <= int(caid_entry[1], 16):
								return True
					except:
						pass

		return False

	boolean = property(getBool)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			self.updateFEdata = False
			if what[1] == iPlayableService.evNewProgramInfo:
				self.updateFEdata = True
			if what[1] == iPlayableService.evEnd:
				self.feraw = self.fedata = None
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL and self.updateFEdata is not None:
			self.updateFEdata = False
			Converter.changed(self, what)
