from sqlalchemy import create_engine, Table, Column, Integer, Unicode, Boolean, MetaData, select
import urlparse

DATABASE_NAME = 'db/data.sqlite'
HTML_DIR = 'data/html/'

class CrawlerDb:

	def __init__(self):
		self.connected = False

	def connect(self):

		self.engine = create_engine('sqlite:///' + DATABASE_NAME)
		self.connection = self.engine.connect()
		self.connected = True if self.connection else False
		self.metadata = MetaData()

		# Define the tables
		self.website_table = Table('website', self.metadata,
			Column('id', Integer, primary_key=True),
			Column('url', Unicode, nullable=False),
			Column('has_crawled', Boolean, default=False),
			Column('emails', Unicode, nullable=True),
		)

		# Create the tables
		self.metadata.create_all(self.engine)

	def add_to_queue(self, url, emails = None):
		if not self.connected:
			return False

		s = select([self.website_table]).where(self.website_table.c.url == url)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result, then this url is not unique
		if len(result) > 0:
# 			print 'Duplicated: %s' % url
			return False

		args = [{'url':unicode(url)}]
		if (emails != None):
			args = [{'url':unicode(url), 'has_crawled':True, 'emails':unicode(",".join(emails))}]
		result = self.connection.execute(self.website_table.insert(), args)
		if result:
			return True
		return False


	def remove_from_queue(self):
		if not self.connected:
			return False
		# queuedeki ilk eleman
		s = select([self.website_table]).limit(1).where(self.website_table.c.has_crawled == False)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# eger result varsa
		if len(result) > 0:

			return result[0]
		return False


	def crawled(self, website, new_emails=None):
		if not self.connected:
			return False
		stmt = self.website_table.update() \
			.where(self.website_table.c.id==website.id) \
			.values(has_crawled=True, emails=new_emails)
		self.connection.execute(stmt)


	def get_all_emails(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		email_set = set()
		for result in results:
			if (result.emails == None):
				continue
			for email in result.emails.split(','):
				email_set.add(email)

		return email_set

	def close(self):
		self.connection.close()


	def save_html(filename, html):
		filename = os.path.join(HTML_DIR, filename)
		file = open(filename,"w+")
		file.writelines(html)
		file.close()
