from summa.summarizer import summarize
import xml.etree.ElementTree as ET
import os, time, threading, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle

categories = ["PODER LEGISLATIVO CAMARA DE DIPUTADOS", "PODER LEGISLATIVO CAMARA DE SENADORES","PODER LEGISLATIVO AUDITORIA SUPERIOR DE LA FEDERACION"]

def summarize_automatic(text):
	return summarize(text, language="spanish")

def summarize_proportion(text,proportion):
	return summarize(text, language="spanish",ratio=proportion)

def summarize_word_count(text,word_count):
	return summarize(text, language="spanish",words=word_count)

def getFileName():
	return datetime.date.today().strftime("XML/%d_%m_%Y.xml")

# After receiving an xml file it will look for the item tags and then obtained all the items that have one of the categories in the categories array. The function will return an array of urls for further actions
def parseXML(XML):
	parser_results = []
	tree = ET.parse(XML)
	elements = tree.getiterator()
	for element in elements:
		if element.tag == "item":
			if element[0].text in categories:
				url = element[1].text
				parser_results.append([url,element[0].text])
	return parser_results

def isToday(XML):
	response = 0
	tree = ET.fromstring(XML)
	elements = tree.getiterator()
	for element in elements:
		if element.tag == "item":
			if element[3].text == datetime.date.today().strftime("%d/%m/%Y"):
				response = 1
			break
	return response

def existsXML(XML):
	return os.path.isfile(getFileName())

def parseEntry(url,category):
	page = urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	title = soup.find("h1", attrs={"class": "Titulo_1"}).text.strip()
	text = ""
	text_divs = soup.findAll("div", attrs={"class": "Texto"})
	if text_divs == []:
		text_divs = soup.findAll("div", attrs={"class": "texto"})
	for div in text_divs:
		text += div.text + "\n"
	if len(text)>20000:
		summary = summarize_word_count(text,len(text)/175)
	else:
		summary = summarize_proportion(text,.3)
	return title, summary , url, category

def obtainXML():
	return urlopen("http://www.dof.gob.mx/sumario.xml").read()

def writeXML(filename,xml):
	try:
		file = open(filename, "w")
		file.write(xml)
		file.close()
		response = True
	except:
		response = False
	return response

# this next function will actuate every 4 hours, it will fetch the xml and check if it exists
def getXMLPeriodically():
	xml = obtainXML()
	filename = getFileName()
	if isToday(xml) and not existsXML(filename):
		print ("new xml")
		writeXML(filename, xml)
		parse_results = parseXML(filename)
		for result in parse_results:
			title, summary , url, category = parseEntry(result[0],result[1])
			add2Pickle(title,summary,url,category)
	else:
		print ("not new xml or old")
	threading.Timer(14400, getXMLPeriodically).start()

def readPickle():
	return pickle.load(open( "congreso.p", "rb" ) )


def add2Pickle(title,summary,url,category):
	try:
		data = pickle.load(open( "congreso.p", "rb" ) )
		new_id = data[len(data)-1]["id"] + 1
	except:
		data = []
		new_id  =  0
	new_data = {
        "id": new_id,
		"category":category,
        "title": title.replace('"',	'&quot;'),
        "summary": summary.replace('"',	'&quot;').replace("\n","<br>"),
        "url": url,
		"yes": 0,
		"no" : 0
    }
	data.append(new_data)
	pickle.dump( data, open( "congreso.p", "wb" ) )

def addVote(id,vote):
	try:
		data = pickle.load(open( "congreso.p", "rb" ) )
		for item in data:
			if(item["id"]==int(id)):
				print("eureka")
				if(vote=="yes"):
					item["yes"] += 1
				elif (vote=="no"):
					item["no"] += 1
		pickle.dump( data, open( "congreso.p", "wb" ) )
		response = 1
	except:
		response = 0
	return response
	