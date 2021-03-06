#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import re
import uuid
from bs4 import *
import lxml
import unicodedata
import urllib2, urllib
import os

page_title=[]
page_url=[]
pdf_urls=[]
uid=[]
content=[]
filename=[]
keywords=[]
pdf_path="../../hrwgc-pdf/data/"
local_pdf = []
category = []
post_path="../_posts/"

cmd = "mkdir -p %s" % (pdf_path)
print "EXEC: " + cmd
os.system(cmd)

con = sqlite3.connect('evernote.sqlite')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS notes")
cur.execute("CREATE TABLE IF NOT EXISTS notes(uid TEXT PRIMARY KEY, title TEXT, created DATETIME, url TEXT, pdf_url TEXT, local_pdf TEXT, filename TEXT, category TEXT, keywords TEXT, content TEXT);")
relpath = "../evernote/data/"
allFiles = os.listdir(relpath)
files = [x for x in allFiles if x.endswith(".html")]

for notefile in files:
	record={}
	record['filename'] = unicode(notefile.decode('ascii','ignore'))
	record['uid'] = uuid.uuid1()
	record['local_pdf'] = ""
	record['category'] = ""
	soup = BeautifulSoup(open(relpath + notefile))
	record['page_title'] = unicodedata.normalize('NFKD',soup.title.string).encode('ascii', 'ignore')
	if soup.head.find('meta', attrs={ 'name' : 'source-url' }) != None:
		record['page_url'] = soup.head.find('meta', attrs={ 'name' : 'source-url' }).get('content')
	elif soup.body.find(text=re.compile("https*://")) != None:
	    record['page_url'] = str(unicode(soup.body.find(text=re.compile("https*://")).string.decode('utf-8')))
	else:
		record['page_url'] = ""
	if len(record['page_url']) != "":
		try:
			response = urllib2.urlopen(record['page_url'])
			vol_html = response.read()
			vol_soup = BeautifulSoup(vol_html)
			if vol_soup.head.find('meta', attrs={ 'name' : 'keywords' }) != None:
				keywords = vol_soup.head.find('meta', attrs={ 'name' : 'keywords' }).get('content').encode('ascii','ignore')
				if soup.head.find('meta', attrs={ 'name' : 'keywords' }) != None:
					keywords = keywords + ', ' + soup.head.find('meta', attrs={ 'name' : 'keywords' }).get('content').encode('ascii','ignore')
				else:
					keywords = keywords
			else:
				keywords = ""
		except:
			keywords = ""	
	else:
		keywords = ""	
	if soup.find('a', attrs={ 'href' : re.compile(".*\.pdf")}) != None:
		record['pdf_urls'] = str(unicode(soup.find('a', attrs={ 'href' : re.compile(".*\.pdf")}).get('href')))
	else:
		record['pdf_urls'] = ""
	record['content'] = unicodedata.normalize('NFKD', soup.body.get_text(" ", strip=True)).encode('ascii', 'ignore')
	if soup.head.find('meta', attrs={ 'name' : 'created' }) != None:
		 record['created'] = re.sub('(.*) \+0000',r'\1', soup.head.find('meta', attrs={ 'name' : 'created' }).get('content')).encode('ascii', 'ignore')
	else:
		record['created'] = ""
#	if len(record['page_url']) > 0:
#		base_keyword_url = "http://tools.davidnaylor.co.uk/keyworddensity/index.php?body=on&bold=on&css=on&duplicate=2&head=on&headings=on&image=on&italic=on&keyword=&link=on&meta=on&phase=4&resubmit=&stopword=on&submit=Check%20Now&title=on&worddetail=on&url="
#		response = urllib2.urlopen(base_keyword_url + urllib.quote_plus(record['page_url']))
#		vol_html = response.read()
#		vol_soup = BeautifulSoup(vol_html)
#		if vol_soup.body.find('table', attrs={ "id" : "phase_1_table"}) != None and vol_soup.body.find('table', attrs={ "id" : "phase_2_table"}) != None:
#			table_1 = vol_soup.body.find('table', attrs={ "id" : "phase_1_table"})
#			table_2 = vol_soup.body.find('table', attrs={ "id" : "phase_2_table"})
#			wordlist_1 = table_1.findAll('td', attrs={ "class" : "cell-highlight"})
#			wordlist_2 = table_2.findAll('td', attrs={ "class" : "cell-highlight"})
			# wordlist = wordlist_1 + wordlist_2
			# words = ""
			# for ix in range(len(wordlist)):
			# 	words = words + "'" +  str(wordlist[ix].text) + "', "
			# if len(keywords) > 0:
			# 	keywords = words + keywords
			# else:
			# 	keywords = words
	if len(record['pdf_urls']) == 0:
		if re.match("^https*://web.docuticker.com.*$", record['page_url']) != None:
			if soup.body.find('a',text=re.compile("Direct link to")) != None:
				record['pdf_urls'] = unicode(soup.body.find('a',text=re.compile("Direct link to")).get('href'))
		elif re.match("^https*://fulltextreports.*$", record['page_url']) != None and record['pdf_urls'] == "":
			try:
				pdf_html = soup.body.p.strong.find("a", attrs={"shape" : "rect"}).get("href")
				response = urllib2.urlopen(pdf_html)
				vol_html = response.read()
				vol_soup = BeautifulSoup(vol_html)
				if vol_soup.find('a', attrs={ 'href' : re.compile("https*://.*\.pdf")}) != None:
					record['pdf_urls'] = unicode(vol_soup.find('a', attrs={ 'href' : re.compile("https*://.*\.pdf")}).get('href'))
			except:
				print("FAIL: " + notefile)
		else:
			try:
				response = urllib2.urlopen(page_url)
				vol_html = response.read()
				vol_soup = BeautifulSoup(vol_html)
				if vol_soup.find('a', attrs={ 'href' : re.compile("https*://.*\.pdf")}) != None:
					record['pdf_urls'] = unicode(vol_soup.find('a', attrs={ 'href' : re.compile("https*://.*\.pdf")}).get('href'))
			except:
				print("FAIL: " + notefile)
	if len(record['pdf_urls']) > 0:
		if len(keywords) == 0:
			record['keywords'] = 'PDF'
		else:
			record['keywords'] = keywords + ', PDF'
		title = re.sub(' ', '-', re.sub(r'[^A-Za-z0-9\-]+', '-', re.sub('[A-Z]', lambda m: m.group(0).lower(), record['page_title'])))
		local_pdf = re.sub(r'[\-]+', r'-', re.sub(r'^(.*)\.html', r'\1', re.sub(r'^\-*([^\-].*[^\-])\-*$',r'\1', re.sub(r'[ ]+', '-', title))))
		if re.match(r'.*\.resources/.*\.pdf', record['pdf_urls']) == None:
			try: 
				# cmd = "wget -t 3 -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11' -O %s %s" % (pdf_path + unicode(record['uid'])  + '-' + local_pdf + '.pdf', record['pdf_urls'])
				# os.system(cmd)
				record['local_pdf'] = pdf_path + unicode(record['uid'])  + '-' + local_pdf + '.pdf'
				record['category'] = "pdf"
			except:
				record['keywords'] = record['keywords'] + ', \'Verify PDF Link\''
		else:
			try:
			#	cmd = "mv \"%s\" \"%s\"" % (relpath + urllib.unquote(record['pdf_urls']), pdf_path + unicode(record['uid']) + '-' + local_pdf + '.pdf')
			#	os.system(cmd)
				record['local_pdf'] = pdf_path + unicode(record['uid'])  + '-' + local_pdf + '.pdf'
				record['category'] = "pdf"
			except:
				record['keywords'] = record['keywords'] + ', \'Verify PDF Link\''
	else:
		record['keywords'] = keywords
	
	cur.execute('insert into notes values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(unicode(record['uid']), record['page_title'], record['created'], record['page_url'], record['pdf_urls'], record['local_pdf'], record['filename'], record['category'], record['keywords'], record['content']))
	con.commit()
	title = re.sub(' ', '-', re.sub(r'[^A-Za-z0-9\-]+', '-', re.sub('[A-Z]', lambda m: m.group(0).lower(), record['page_title'])))
	if len(re.sub(r'[\-]+', r'-', re.sub(r'^(.*)\.html', r'\1', re.sub(r'^\-*([^\-].*[^\-])\-*$',r'\1', re.sub(r'[ ]+', '-', title))))) > 0:
		jekyll = str(post_path + re.sub(r'([0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}).*', r'\1', record['created']) + '-' + re.sub(r'[\-]+', r'-', re.sub(r'^(.*)\.html', r'\1', re.sub(r'^\-*([^\-].*[^\-])\-*$',r'\1', re.sub(r'[ ]+', '-', title)))) + ".md")
	else: 
		jekyll = str(post_path + unicode(record['uid']) + '.md')
	#fin
	cmd = "echo \'---\' >> \"%s\"" % (jekyll)
	os.system(cmd)
	if len(unicode(record['uid'])) > 0:
		cmd = "echo \'uid: \"%s\"\' >> \"%s\"" % (unicode(record['uid']), jekyll)
		os.system(cmd)

	if len(record['page_title']) > 0:
		cmd = "echo \'title: \"%s\"\' >> \"%s\"" % (re.sub(r'([\'\"])', r'', record['page_title']), jekyll)
		os.system(cmd)

	if len(record['created']) > 0:
		cmd = "echo \'created: \"%s\"\' >> \"%s\"" % (record['created'], jekyll)
		os.system(cmd)

	if len(record['page_url']) > 0:
		cmd = "echo \'page_url: \"%s\"\' >> \"%s\"" % (record['page_url'], jekyll)
		os.system(cmd)

	if len(record['pdf_urls']) > 0:
		cmd = "echo \'pdf_urls: \"%s\"\' >> \"%s\"" % (record['pdf_urls'], jekyll)
		os.system(cmd)

	if len(record['local_pdf']) > 0:
		cmd = "echo \'local_pdf: \"%s\"\' >> \"%s\"" % (record['local_pdf'], jekyll)
		os.system(cmd)

	if len(record['filename']) > 0:
		cmd = "echo \'filename: \"%s\"\' >> \"%s\"" % (re.sub(r'([\'\"])', '', record['filename']), jekyll)
		os.system(cmd)

	if len(record['category']) > 0:
		cmd = "echo \'category: \"%s\"\' >> \"%s\"" % (record['category'], jekyll)
		os.system(cmd)

	if len(record['keywords']) > 0:
		cmd = "echo \'tags: \' >> \"%s\"" % (jekyll)
		os.system(cmd)
		cmd = "echo '%s' >> \"%s\"" % (re.sub(',[ ]*',r'\n - ', re.sub(r'^,*', ' - ', re.sub(r'([\'\"])', '', record['keywords']))), jekyll)
		os.system(cmd)
	cmd = "echo \'---\' >> \"%s\"" % (jekyll)
	os.system(cmd)
