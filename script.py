from summa.summarizer import summarize
import xml.etree.ElementTree as ET
import os, time, threading, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

categories = ["PODER LEGISLATIVO CAMARA DE DIPUTADOS", "PODER LEGISLATIVO CAMARA DE SENADORES"]

def summarize_automatic(text):
	return summarize(text, language='spanish')

def summarize_proportion(text,proportion):
	return summarize(text, language='spanish',ratio=proportion)

def getFileName():
	return datetime.date.today().strftime('XML/%d_%b_%Y.xml')

# After receiving an xml file it will look for the item tags and then obtained all the items that have one of the categories in the categories array. The function will return an array of urls for further actions
def parseXML(XML):
	parser_results = []
	tree = ET.parse(XML)
	elements = tree.getiterator()
	for element in elements:
		if element.tag == 'item':
			if element[0].text in categories:
				url = element[1].text
				parser_results.append(url)

def isToday(XML):
	response = 0
	tree = ET.parse(XML)
	elements = tree.getiterator()
	for element in elements:
		if element.tag == 'item':
			if element[3].text == datetime.date.today().strftime('%d/%m/%Y'):
				response = 1
			break
	return response

def existsXML(XML):
	return os.path.isfile(getFileName())

def parseEntry(url):
	page = urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	title = soup.find("h1", attrs={"class": "Titulo_1"}).text.strip()
	text = ""
	text_divs = soup.findAll("div", attrs={"class": "Texto"})
	for div in text_divs:
		text += div.text + "\n"
	return title, text

def obtainXML():
	return urlopen("http://www.dof.gob.mx/sumario.xml").read()

def writeXML(filename,xml):
	try:
		file = open(filename, 'w')
		file.write(xml)
		file.close()
		response = True
	except:
		response = False
	return response

# this next function will actuate every 4 hours, it will fetch the xml and check if it exists
def getXMLPeriodically():
	threading.Timer(14400, getXMLPeriodically).start()

getXMLPeriodically()