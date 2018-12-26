#!/usr/bin/python
from settings import LOGGING
import logging, logging.config
import urllib, urllib2
import re, urlparse
import traceback
from database import CrawlerDb
import csv
import os
import sys

# Logging
logging.config.dictConfig(LOGGING)
log = logging.getLogger("CRAWLER_LOG")

regex_google_adurl = re.compile('adurl=(.*?)"')
regex_google_url = re.compile('url\?q=(.*?)&amp;sa=')
regex_email = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
regex_url = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')

EMAILS_FILE = 'data/all_emails.csv'

# Set up the database
db = CrawlerDb()
db.connect()


def crawl(key,count):

	log.info("-"*40)
	log.info("Searhcing Keywords of  %s  at Google" % key.decode('utf-8'))
	log.info("-"*40)

	for i in range(0, count, 10):
		query = {'q': key}
		url = 'http://www.google.com/search?' + urllib.urlencode(query) + '&start=' + str(i)
		data = get_source(url)
		for url in regex_google_url.findall(data):
			db.add_to_queue(unicode(url))
		for url in regex_google_adurl.findall(data):
			db.add_to_queue(unicode(url))

	# Crawl each of the search result

	while (True):
		# remove_from_queue an uncrawled webpage from db
		uncrawled = db.remove_from_queue()
		if (uncrawled == False):
			break
		email_set = find_emails_subsite(uncrawled.url)
		if (len(email_set) > 0):
			db.crawled(uncrawled, ",".join(list(email_set)))
		else:
			db.crawled(uncrawled, None)

def get_source(url):

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Just-Crawling 0.1')
	request = None
	status = 0
	try:
		log.info("Crawling %s" % url)
		request = urllib2.urlopen(req)
	except urllib2.URLError, e:
		log.error("Exception at url: %s\n%s" % (url, e))
	except urllib2.HTTPError, e:
		status = e.code
	except Exception, e:
		return
	if status == 0:
		status = 200

	try:
		source = request.read()
	except Exception, e:
		return

	return str(source)


def find_emails_subsite(url):

	source = get_source(url)
	email_set = find_emails_in_source(source)

	if (len(email_set) > 0):
		return email_set

	else:
		# Crawl subsites
		log.info('No email at site.. proceeding to crawl subsites')

		links = find_links(url, source)
		for link in links:

			source = get_source(link)
			if (source == None):
				continue
			email_set = find_emails_in_source(source)
			db.add_to_queue(link, list(email_set))

		# We return an empty set
		return set()


def find_emails_in_source(source):
	if (source == None):
		return set()
	email_set = set()
	for email in regex_email.findall(source):
		email_set.add(email)
	return email_set


def find_links(url, source):
	if (source == None):
		return set()
	url = urlparse.urlparse(url)
	links = regex_url.findall(source)
	link_set = set()
	for link in links:
		if link == None:
			continue
		try:
			link = str(link)
			if link.startswith("/"):
				link_set.add('http://'+url.netloc+link)
			elif link.startswith("http") or link.startswith("https"):
				if (link.find(url.netloc)):
					link_set.add(link)
			elif link.startswith("#"):
				continue
			else:
				link_set.add(urlparse.urljoin(url.geturl(),link))
		except Exception, e:
			pass

	return link_set

def sort():
    path = '/home/mekhti/Downloads/web mining/python-email-crawler-master/data/all_emails.csv'
    output = open('emails.csv', 'wb')
    writer = csv.writer(output)

    with open(path, "r") as csvfile:
     	csv_reader = csv.reader(csvfile, delimiter='\n')
     	for row in csv_reader:
            a=row
            if (not str(a).endswith("png']")):
                writer.writerow(row)

def print_emails():
	path = '/home/mekhti/Downloads/web mining/python-email-crawler-master/emails.csv'
	with open(path,'r') as f:
		for line in f:
			print line


try:
	arg = sys.argv[1].lower()

	if (arg == '--emails') or (arg == '-e'):
		# Get all the emails and save in a CSV
		log.info("="*40)
		log.info("Processing...")
		emails = db.get_all_emails()
		log.info("There are %d emails" % len(emails))
		file = open(EMAILS_FILE, "w+")
		file.writelines("\n".join(emails))
		file.close()
		log.info("All emails saved to ./data/emails.csv")
		log.info("="*40)
		sort()
		print_emails()

	else:
		count = int(sys.argv[2])
		crawl(arg,count)

except KeyboardInterrupt:
	log.error("KeyboardInterrupt")
	sys.exit()
except Exception, e:
	log.error("EXCEPTION: %s " % e)
	traceback.print_exc()
