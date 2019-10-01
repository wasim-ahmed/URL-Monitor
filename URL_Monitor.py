'''
This program reads each Link mentioned in configuration file. Starts a Thread and put it to monitor @ specified frequency.
If the Link is down it will shoot the email to the notifiers.
'''

from multiprocessing import Process
import time
import urllib.request
import smtplib
from xml.dom.minidom import parse
import xml.dom.minidom

class Container:
	def __init__(self):
		self.Application = ""
		self.Description = ""
		self.URL = ""
		self.Up_Time_Polling = 0
		self.Down_Time_Polling = 0
		self.Notifiers_id = []

			
def thread(Cy,user,pwd):
	
	for id in range(len(Cy.Notifiers_id)):
		mail(Cy.Notifiers_id[id],Cy.URL,False,user,pwd,Cy.Application)

	while True:

		try:
			conn = urllib.request.urlopen(Cy.URL)
		except urllib.error.HTTPError as e:
			# Return code error (e.g. 404, 501, ...)
			# ...
			#print('HTTPError: {}'.format(e.code))
			for idx in range(len(Cy.Notifiers_id)):
				mail(Cy.Notifiers_id[idx],Cy.URL,True,user,pwd,Cy.Application)
			time.sleep(int(Cy.Down_Time_Polling))#seconds
		except urllib.error.URLError as e:
			# Not an HTTP-specific error (e.g. connection refused)
			# ...
			#print('URLError hai: {}'.format(e.reason))
			for idy in range(len(Cy.Notifiers_id)):	
				mail(Cy.Notifiers_id[idy],Cy.URL,True,user,pwd,Cy.Application)
			time.sleep(int(Cy.Down_Time_Polling))#seconds
		else:
			# 200
			# ...
			print("success:" + Cy.URL)
			time.sleep(int(Cy.Up_Time_Polling))#seconds


def mail(address,url,error,user,pwd,application):
	
	fromaddr = 'abc@xyz.com' # sender's email address
	toaddrs = address
	
	header = ("From: URL Monitor Admin  \r\nTo: %s \r\nSubject: URL Monitor Active :: %s \r\n\r\n " % (toaddrs,application))
	
	if error == True:
		body = "Hi,\n Your URL: " + url + " is down. Please check with system \n\nThanks,\nAdmin "
	else:
		body = "Hi,\n Your URL: " + url + " is put to monitor you will be informed in case of any discrepancies. \n\nThanks,\nAdmin "

	mail = header + body

	server = smtplib.SMTP('SMTP Server address',port)
	server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.ehlo
	server.login(user,pwd)
	server.sendmail(fromaddr, toaddrs, mail)
	server.quit()
			
user = " "
pwd = " "
		
if __name__ == '__main__':

	user = input("Enter your User Name:")
	pwd = input("Enter your PASSWORD:")
	
	Cx = Container();
	# Open XML document using minidom parser & read the configuration file
	DOMTree = xml.dom.minidom.parse("URL_Config.xml")
	collection = DOMTree.documentElement
	if collection.hasAttribute("program"):
		print ("Root element : %s" % collection.getAttribute("program"))

	links = collection.getElementsByTagName("LINK")

	for link in links:
		
		if link.hasAttribute("title"):
			print ("Title: %s" % link.getAttribute("title"))

		Application = link.getElementsByTagName('Application')[0]
		Cx.Application = Application.childNodes[0].data
		
		Description = link.getElementsByTagName('Description')[0]
		Cx.Description = Description.childNodes[0].data
		
		URL = link.getElementsByTagName('URL')[0]
		Cx.URL = URL.childNodes[0].data
		
		Up_Time_Polling = link.getElementsByTagName('Up_Time_Polling')[0]
		Cx.Up_Time_Polling = Up_Time_Polling.childNodes[0].data
		
		Down_Time_Polling = link.getElementsByTagName('Down_Time_Polling')[0]
		Cx.Down_Time_Polling = Down_Time_Polling.childNodes[0].data
		
		Notifiers = link.getElementsByTagName('Notifiers')
		for notifier in Notifiers:
			Cx.Notifiers_id.append(notifier.attributes['id'].value)

		
		p = Process(target=thread, args=(Cx,user,pwd))
		p.start()
		Cx.Notifiers_id.clear()
		time.sleep(10)#seconds required,  for each thread to finish it's processing 
		
		
	p.join()		